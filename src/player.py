"""
Player class - handles player movement, jumping, and collisions with sprite animations
"""
import pygame
import os
from src.constants import DIFFICULTY_SETTINGS, SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_PLAYER

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, difficulty="MEDIUM"):
        super().__init__()
        self.start_x = x
        self.start_y = y
        
        # Get difficulty settings
        settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["MEDIUM"])
        self.gravity = settings["GRAVITY"]
        self.player_speed = settings["PLAYER_SPEED"]
        self.jump_power = settings["JUMP_POWER"]
        
        # Animation states
        self.state = "idle"  # idle, running, jumping, falling, double_jumping, wall_jumping
        self.animation_frame = 0
        self.animation_speed = 0.15
        self.facing_right = True
        
        # Load all sprite sheets with proper dimension handling
        self.idle_sprites = self._load_sprite_sheet("idle.png", (32, 32))          # 11 frames
        self.run_sprites = self._load_sprite_sheet("run.png", (32, 32))            # 12 frames
        self.jump_sprite = self._load_image("jump.png")                            # 1 frame (32x32)
        self.fall_sprite = self._load_image("fall.png")                            # 1 frame (32x32)
        self.double_jump_sprites = self._load_sprite_sheet("double_jump.png", (32, 32))  # 6 frames
        self.wall_jump_sprites = self._load_sprite_sheet("wall_jump.png", (32, 32))     # 5 frames
        
        # Create player sprite
        self.image = (self.idle_sprites[0] if self.idle_sprites else None) or pygame.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Physics
        self.velocity_y = 0
        self.velocity_x = 0
        self.is_jumping = False
        self.on_ground = False
        self.wall_jumping = False
        self.double_jump_available = True
    
    def _load_image(self, filename):
        """Load a single image from the project root"""
        try:
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
            image = pygame.image.load(path).convert_alpha()
            return image
        except Exception as e:
            print(f"Could not load {filename}: {e}")
            return None
    
    def _load_sprite_sheet(self, filename, frame_size):
        """Load a sprite sheet and split it into individual frames"""
        try:
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
            sheet = pygame.image.load(path).convert_alpha()
            
            frames = []
            frame_width, frame_height = frame_size
            num_frames = sheet.get_width() // frame_width
            
            for i in range(num_frames):
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
                frames.append(frame)
            
            return frames if frames else None
        except Exception as e:
            print(f"Could not load {filename}: {e}")
            return None
    
    def _get_current_sprite(self):
        """Get the current sprite based on animation state"""
        sprite = None
        
        if self.state == "idle" and self.idle_sprites:
            frame_idx = int(self.animation_frame) % len(self.idle_sprites)
            sprite = self.idle_sprites[frame_idx]
        elif self.state == "running" and self.run_sprites:
            frame_idx = int(self.animation_frame) % len(self.run_sprites)
            sprite = self.run_sprites[frame_idx]
        elif self.state == "jumping":
            sprite = self.jump_sprite
        elif self.state == "falling":
            sprite = self.fall_sprite
        elif self.state == "double_jumping" and self.double_jump_sprites:
            frame_idx = int(self.animation_frame) % len(self.double_jump_sprites)
            sprite = self.double_jump_sprites[frame_idx]
        elif self.state == "wall_jumping" and self.wall_jump_sprites:
            frame_idx = int(self.animation_frame) % len(self.wall_jump_sprites)
            sprite = self.wall_jump_sprites[frame_idx]
        
        if not sprite:
            sprite = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        # Flip if facing left
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        return sprite
    
    def move_left(self):
        """Move player left"""
        self.velocity_x = -self.player_speed
        self.facing_right = False
    
    def move_right(self):
        """Move player right"""
        self.velocity_x = self.player_speed
        self.facing_right = True
    
    def jump(self):
        """Make player jump if on ground"""
        if self.on_ground:
            self.velocity_y = -self.jump_power
            self.is_jumping = True
            self.on_ground = False
            self.state = "jumping"
    
    def update(self):
        """Update player position and physics"""
        # Apply gravity
        self.velocity_y += self.gravity
        
        # Cap falling velocity
        if self.velocity_y > 15:
            self.velocity_y = 15
        
        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Update animation frame
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 12:  # Max frames in run sprite sheet
            self.animation_frame = 0
        
        # Update state for animation
        if self.velocity_y < -2:
            self.state = "jumping"
        elif self.velocity_y > 1 and not self.on_ground:
            self.state = "falling"
        elif self.velocity_x != 0 and self.on_ground:
            self.state = "running"
        else:
            self.state = "idle"
        
        # Update sprite based on state
        self.image = self._get_current_sprite()
        
        # Reset velocity for next frame
        self.velocity_x = 0
        
        # Screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH + 2000:
            self.rect.right = SCREEN_WIDTH + 2000
        
        # Reset jumping flag if falling
        if self.velocity_y > 0:
            self.is_jumping = False
        
        # Reset ground flag each frame
        self.on_ground = False
    
    def check_collision(self, platform):
        """Check collision with a platform"""
        if self.rect.colliderect(platform.rect):
            # Coming from above (standing on platform)
            if self.velocity_y >= 0 and self.rect.bottom <= platform.rect.top + 15:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True
                self.is_jumping = False
                self.state = "idle"
                return True
            # Coming from below (hitting head)
            elif self.velocity_y < 0 and self.rect.top >= platform.rect.bottom - 10:
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
                return True
            # Coming from left side
            elif self.velocity_x > 0 and self.rect.right <= platform.rect.left + 10:
                self.rect.right = platform.rect.left
                return True
            # Coming from right side
            elif self.velocity_x < 0 and self.rect.left >= platform.rect.right - 10:
                self.rect.left = platform.rect.right
                return True
        return False
    
    def reset(self):
        """Reset player to start position"""
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False
        self.on_ground = False
        self.state = "idle"
        self.animation_frame = 0
    
    def draw(self, surface):
        """Draw player on screen"""
        surface.blit(self.image, self.rect)
