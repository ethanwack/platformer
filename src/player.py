"""
Player class - handles player movement, jumping, and collisions
"""
import pygame
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
        self.state = "idle"  # idle, running, jumping, falling
        self.animation_frame = 0
        self.animation_speed = 0.15
        self.facing_right = True
        
        # Create player sprite
        self.image = self._create_character_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Physics
        self.velocity_y = 0
        self.velocity_x = 0
        self.is_jumping = False
        self.on_ground = False
    
    def _create_character_sprite(self, state="idle", frame=0):
        """Create an animated character sprite"""
        # Create a character with animation frames
        image = pygame.Surface((32, 48), pygame.SRCALPHA)
        
        # Head (circle)
        pygame.draw.circle(image, (255, 200, 100), (16, 12), 8)
        
        # Body (rectangle)
        pygame.draw.rect(image, COLOR_PLAYER, (12, 20, 20, 16))
        
        # Eyes
        pygame.draw.circle(image, (0, 0, 0), (13, 10), 2)
        pygame.draw.circle(image, (0, 0, 0), (19, 10), 2)
        
        # Smile
        pygame.draw.arc(image, (0, 0, 0), (13, 10, 6, 4), 0, 3.14, 1)
        
        # Animation based on state
        if state == "jumping":
            # Jumping pose - legs spread
            pygame.draw.line(image, (255, 200, 100), (12, 24), (2, 32), 2)
            pygame.draw.line(image, (255, 200, 100), (20, 24), (30, 32), 2)
            pygame.draw.line(image, COLOR_PLAYER, (14, 36), (10, 45), 2)
            pygame.draw.line(image, COLOR_PLAYER, (18, 36), (22, 45), 2)
        elif state == "running":
            # Running pose - alternating legs
            offset = 2 if frame % 2 == 0 else -2
            pygame.draw.line(image, (255, 200, 100), (12, 24), (4 + offset, 28), 2)
            pygame.draw.line(image, (255, 200, 100), (20, 24), (28 - offset, 28), 2)
            pygame.draw.line(image, COLOR_PLAYER, (14, 36), (12 + offset * 1.5, 45), 2)
            pygame.draw.line(image, COLOR_PLAYER, (18, 36), (20 - offset * 1.5, 45), 2)
        else:  # idle
            # Standing pose
            pygame.draw.line(image, (255, 200, 100), (12, 24), (6, 28), 2)
            pygame.draw.line(image, (255, 200, 100), (20, 24), (26, 28), 2)
            pygame.draw.line(image, COLOR_PLAYER, (14, 36), (12, 45), 2)
            pygame.draw.line(image, COLOR_PLAYER, (18, 36), (20, 45), 2)
        
        # Flip if facing left
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)
        
        return image
    
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
        
        # Update animation
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 2:
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
        self.image = self._create_character_sprite(self.state, int(self.animation_frame))
        
        # Reset velocity for next frame
        self.velocity_x = 0
        
        # Screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH + 2000:  # Allow going far right with world
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
