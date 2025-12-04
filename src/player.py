"""
Player class - clean implementation with sprite loading, physics and simple attack.
"""
import pygame
import os
from src.constants import DIFFICULTY_SETTINGS, SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_PLAYER


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, difficulty="MEDIUM"):
        super().__init__()
        self.start_x = x
        self.start_y = y

        # Difficulty settings
        settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["MEDIUM"])
        self.gravity = settings["GRAVITY"]
        self.player_speed = settings["PLAYER_SPEED"]
        self.jump_power = settings["JUMP_POWER"]

        # Animation / sprite data
        self.state = "idle"
        self.animation_frame = 0.0
        self.animation_speed = 0.15
        self.facing_right = True

        # Load sprites
        self.idle_sheet = self._load_image("Start (Idle).png")
        self.moving_frames = self._load_moving_sprites("Start (Moving) (64x64).png")
        self.small_idle = self._load_sprite_sheet("idle.png", (32, 32))
        self.small_run = self._load_sprite_sheet("run.png", (32, 32))
        self.small_jump = self._load_image("jump.png")
        self.small_fall = self._load_image("fall.png")

        # initial image
        if self.idle_sheet:
            self.image = self.idle_sheet
        elif self.small_idle:
            self.image = self.small_idle[0]
        else:
            self.image = self._create_fallback_sprite()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Physics
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.is_jumping = False
        self.jump_buffer = 0  # Frames remaining in jump buffer
        self.jump_buffer_max = 6  # Allow jump input up to 6 frames after landing

        # Weapon/attack
        self.weapon = None
        self.ammo = 0
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 12

        # Health
        self.max_health = 3
        self.health = self.max_health
        self.invincibility_timer = 0
        self.invincibility_duration = 120  # Frames of invincibility after hit (2 seconds at 60 FPS)

    def _create_fallback_sprite(self):
        surf = pygame.Surface((32, 48), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 200, 100), (16, 12), 8)
        pygame.draw.rect(surf, COLOR_PLAYER, (12, 20, 20, 16))
        return surf

    def _load_image(self, filename):
        try:
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
            return pygame.image.load(path).convert_alpha()
        except Exception:
            return None

    def _load_moving_sprites(self, filename):
        try:
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
            sheet = pygame.image.load(path).convert_alpha()
            fw = 64
            fh = sheet.get_height()
            frames = []
            for i in range(sheet.get_width() // fw):
                f = pygame.Surface((fw, fh), pygame.SRCALPHA)
                f.blit(sheet, (0, 0), (i * fw, 0, fw, fh))
                frames.append(f)
            return frames
        except Exception:
            return None

    def _load_sprite_sheet(self, filename, frame_size):
        try:
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
            sheet = pygame.image.load(path).convert_alpha()
            fw, fh = frame_size
            frames = []
            for i in range(sheet.get_width() // fw):
                f = pygame.Surface((fw, fh), pygame.SRCALPHA)
                f.blit(sheet, (0, 0), (i * fw, 0, fw, fh))
                frames.append(f)
            return frames
        except Exception:
            return None

    def move_left(self):
        self.velocity_x = -self.player_speed
        self.facing_right = False

    def move_right(self):
        self.velocity_x = self.player_speed
        self.facing_right = True

    def jump(self):
        if self.on_ground or self.jump_buffer > 0:
            self.velocity_y = -self.jump_power
            self.on_ground = False
            self.is_jumping = True
            self.jump_buffer = 0  # Consume the buffer

    def attack(self):
        if self.weapon and self.ammo > 0 and not self.attacking:
            self.attacking = True
            self.attack_timer = 0
            self.ammo -= 1

    def get_attack_rect(self):
        if not self.attacking:
            return None
        w = 32
        h = 20
        if self.facing_right:
            ax = self.rect.right
        else:
            ax = self.rect.left - w
        ay = self.rect.centery - h // 2
        return pygame.Rect(ax, ay, w, h)

    def take_damage(self, amount=1):
        """Reduce health and apply invincibility frames. Returns True if player dies."""
        if self.invincibility_timer <= 0:
            self.health -= amount
            self.invincibility_timer = self.invincibility_duration
            return self.health <= 0
        return False

    def is_invincible(self):
        """Check if player is currently invincible."""
        return self.invincibility_timer > 0

    def update(self):
        # physics
        self.velocity_y += self.gravity
        if self.velocity_y > 15:
            self.velocity_y = 15
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # animation frame tick
        self.animation_frame += self.animation_speed

        # state
        if self.velocity_y < -2:
            self.state = "jumping"
        elif self.velocity_y > 1 and not self.on_ground:
            self.state = "falling"
        elif self.velocity_x != 0 and self.on_ground:
            self.state = "running"
        else:
            self.state = "idle"

        # choose image - prioritize small sprites for consistency, fall back to single images
        img = None
        if self.state == "idle":
            # Use small_idle sprite sheet if available
            if self.small_idle:
                frame_idx = int(self.animation_frame) % len(self.small_idle)
                img = self.small_idle[frame_idx]
            elif self.idle_sheet:
                img = self.idle_sheet
        elif self.state == "running":
            # Use small_run sprite sheet if available
            if self.small_run:
                frame_idx = int(self.animation_frame) % len(self.small_run)
                img = self.small_run[frame_idx]
            elif self.moving_frames:
                frame_idx = int(self.animation_frame) % len(self.moving_frames)
                img = self.moving_frames[frame_idx]
        elif self.state == "jumping":
            img = self.small_jump if self.small_jump else None
        elif self.state == "falling":
            img = self.small_fall if self.small_fall else None

        if img:
            if not self.facing_right:
                img = pygame.transform.flip(img, True, False)
            self.image = img
            # Update rect to match current image size, but preserve position
            old_bottom = self.rect.bottom
            old_left = self.rect.left
            self.rect = self.image.get_rect()
            self.rect.bottom = old_bottom
            self.rect.left = old_left
        else:
            # Fallback if no sprite is available - create a simple square
            if not hasattr(self, '_fallback_created'):
                self.image = self._create_fallback_sprite()
                self._fallback_created = True

        # reset horizontal velocity
        self.velocity_x = 0

        # clamp
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH + 2000:
            self.rect.right = SCREEN_WIDTH + 2000

        # reset flags
        if self.velocity_y > 0:
            self.is_jumping = False
        self.on_ground = False
        
        # Manage jump buffer - decrement each frame, reset when landing
        self.jump_buffer = max(0, self.jump_buffer - 1)

        # attack timing
        if self.attacking:
            self.attack_timer += 1
            if self.attack_timer >= self.attack_duration:
                self.attacking = False
                self.attack_timer = 0

        # invincibility timer
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

    def check_collision(self, platform):
        if self.rect.colliderect(platform.rect):
            # Determine which side of the platform the player is coming from
            # by checking where the player was before this frame
            
            # How much are we overlapping?
            overlap_top = self.rect.bottom - platform.rect.top      # Distance from player bottom to platform top
            overlap_bottom = platform.rect.bottom - self.rect.top   # Distance from platform bottom to player top
            overlap_left = self.rect.right - platform.rect.left     # Distance from player right to platform left
            overlap_right = platform.rect.right - self.rect.left    # Distance from platform right to player left
            
            # Player is falling onto platform from above
            if overlap_top > 0 and overlap_top < overlap_bottom and self.velocity_y >= 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True
                self.is_jumping = False
                self.jump_buffer = self.jump_buffer_max  # Refresh jump buffer on landing
                return True
            
            # Player is jumping into platform from below
            elif overlap_bottom > 0 and overlap_bottom < overlap_top and self.velocity_y < 0:
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
                return True
            
            # Player is hitting platform from the right side (moving left into it)
            elif overlap_left > 0 and overlap_left < overlap_right and self.velocity_x < 0:
                self.rect.left = platform.rect.right
                return True
            
            # Player is hitting platform from the left side (moving right into it)
            elif overlap_right > 0 and overlap_right < overlap_left and self.velocity_x > 0:
                self.rect.right = platform.rect.left
                return True
        
        return False

    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.is_jumping = False
        self.state = "idle"
        self.animation_frame = 0
        self.attacking = False
        self.jump_buffer = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

