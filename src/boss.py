"""
Boss class - represents boss enemies with health and special mechanics
"""
import pygame
import os
from src.constants import SCREEN_HEIGHT, DIFFICULTY_SETTINGS

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, level, difficulty="MEDIUM"):
        super().__init__()
        self.level = level  # Boss level 1-5
        self.difficulty = difficulty
        self.x_pos = x
        self.y_pos = y
        
        # Get difficulty settings
        settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["MEDIUM"])
        
        # Boss stats scale with level and difficulty
        self.base_health = 3 + level
        if difficulty == "HARD":
            self.base_health += 2
        elif difficulty == "EASY":
            self.base_health = max(2, self.base_health - 1)
        
        self.health = self.base_health
        self.max_health = self.base_health
        
        # Size scales with level
        self.width = 64
        self.height = 64
        
        # Load sprite sheets for animations
        self.appearing_sprites = self._load_sprite_sheet("Appearing (96x96).png", (96, 96))  # 7 frames
        self.disappearing_sprites = self._load_sprite_sheet("Desappearing (96x96).png", (96, 96))  # 7 frames
        
        # Boss animation state
        self.animation_frame = 0
        self.animation_speed = 0.15
        self.boss_state = "idle"  # appearing, idle, disappearing, defeated
        
        # Create boss sprite
        self.image = self._create_boss_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Boss movement
        self.speed = 1.5 + (level * 0.3)
        if difficulty == "HARD":
            self.speed += 1
        self.direction = 1
        self.patrol_left = max(100, x - 150)
        self.patrol_right = min(900, x + 150)
        
        # Attack pattern
        self.attack_counter = 0
        self.attack_frequency = max(60 - level * 10, 30)
        self.is_attacking = False
        
        # Jump ability
        self.jump_timer = 0
        self.can_jump = True
        self.velocity_y = 0
        self.gravity = 0.4
    
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
    
    def _create_boss_sprite(self):
        """Create a boss sprite that gets bigger with level"""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Boss body
        color = (100 + self.level * 20, 50, 50)
        pygame.draw.rect(image, color, (5, 15, self.width - 10, self.height - 25))
        
        # Boss head
        pygame.draw.circle(image, color, (self.width // 2, 12), 8 + self.level)
        
        # Eyes (angry)
        pygame.draw.circle(image, (255, 0, 0), (self.width // 2 - 6, 10), 3)
        pygame.draw.circle(image, (255, 0, 0), (self.width // 2 + 6, 10), 3)
        
        # Evil mouth
        pygame.draw.line(image, (255, 0, 0), (self.width // 2 - 4, 14), (self.width // 2 + 4, 14), 2)
        
        # Spikes on back for higher levels
        if self.level >= 2:
            spike_color = (150, 50, 50)
            for i in range(self.level):
                spike_x = 10 + i * (self.width - 20) // self.level
                pygame.draw.polygon(image, spike_color, [
                    (spike_x, 15),
                    (spike_x - 3, 5),
                    (spike_x + 3, 5)
                ])
        
        return image
    
    def update(self):
        """Update boss position and behavior"""
        if self.boss_state == "appearing" and self.appearing_sprites:
            self.animation_frame += self.animation_speed
            if self.animation_frame >= len(self.appearing_sprites):
                self.boss_state = "idle"
                self.animation_frame = 0
            else:
                frame_idx = int(self.animation_frame)
                self.image = self.appearing_sprites[frame_idx]
        
        elif self.boss_state == "disappearing" and self.disappearing_sprites:
            self.animation_frame += self.animation_speed
            if self.animation_frame >= len(self.disappearing_sprites):
                self.boss_state = "defeated"
                self.kill()
            else:
                frame_idx = int(self.animation_frame)
                self.image = self.disappearing_sprites[frame_idx]
        
        elif self.boss_state == "idle":
            # Patrol movement
            self.rect.x += self.speed * self.direction
            
            # Turn around at patrol boundaries
            if self.rect.left <= self.patrol_left or self.rect.right >= self.patrol_right:
                self.direction *= -1
            
            # Apply gravity
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            
            # Ground collision
            if self.rect.bottom >= SCREEN_HEIGHT - 40:
                self.rect.bottom = SCREEN_HEIGHT - 40
                self.velocity_y = 0
                self.can_jump = True
            
            # Jump logic
            self.jump_timer += 1
            if self.jump_timer > 120 and self.can_jump:
                self.velocity_y = -8
                self.can_jump = False
                self.jump_timer = 0
            
            # Attack pattern
            self.attack_counter += 1
            if self.attack_counter >= self.attack_frequency:
                self.is_attacking = True
                self.attack_counter = 0
            else:
                self.is_attacking = False
    
    def take_damage(self, amount=1):
        """Boss takes damage and triggers disappearing animation"""
        self.health -= amount
        if self.health <= 0:
            self.boss_state = "disappearing"
            self.animation_frame = 0
        return self.health <= 0
    
    def is_defeated(self):
        """Check if boss is defeated"""
        return self.boss_state == "defeated"
    
    def get_health_percentage(self):
        """Get health as a percentage"""
        return max(0, (self.health / self.max_health) * 100)
    
    def draw(self, surface):
        """Draw boss on screen"""
        surface.blit(self.image, self.rect)
        
        # Draw health bar only if not using sprite animations
        if self.boss_state == "idle":
            bar_width = 100
            bar_height = 8
            bar_x = self.rect.centerx - bar_width // 2
            bar_y = self.rect.top - 20
            
            # Background bar
            pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            
            # Health bar
            health_width = int(bar_width * self.get_health_percentage() / 100)
            pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))
            
            # Border
            pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
    
    def kill(self):
        """Remove boss from game"""
        super().kill()
