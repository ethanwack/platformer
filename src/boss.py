"""
Boss class - represents boss enemies with health and special mechanics
"""
import pygame
from src.constants import SCREEN_HEIGHT, DIFFICULTY_SETTINGS

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, level, difficulty="MEDIUM"):
        super().__init__()
        self.level = level  # Boss level 1-5
        self.difficulty = difficulty
        
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
        self.width = 40 + (level * 5)
        self.height = 50 + (level * 3)
        
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
        self.attack_frequency = max(60 - level * 10, 30)  # Attacks more frequently on higher levels
        self.attack_range = 150 + (level * 20)
        self.is_attacking = False
        
        # Jump ability
        self.jump_timer = 0
        self.can_jump = True
        self.velocity_y = 0
        self.gravity = 0.4
    
    def _create_boss_sprite(self):
        """Create a boss sprite that gets bigger with level"""
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Boss body
        color = (100 + self.level * 20, 50, 50)
        pygame.draw.rect(image, color, (5, 10, self.width - 10, self.height - 15))
        
        # Boss head
        pygame.draw.circle(image, color, (self.width // 2, 10), 8 + self.level)
        
        # Eyes (angry)
        pygame.draw.circle(image, (255, 0, 0), (self.width // 2 - 6, 8), 3)
        pygame.draw.circle(image, (255, 0, 0), (self.width // 2 + 6, 8), 3)
        
        # Evil mouth
        pygame.draw.line(image, (255, 0, 0), (self.width // 2 - 4, 12), (self.width // 2 + 4, 12), 2)
        
        # Spikes on back for higher levels
        if self.level >= 2:
            spike_color = (150, 50, 50)
            for i in range(self.level):
                spike_x = 10 + i * (self.width - 20) // self.level
                pygame.draw.polygon(image, spike_color, [
                    (spike_x, 10),
                    (spike_x - 3, 0),
                    (spike_x + 3, 0)
                ])
        
        return image
    
    def update(self):
        """Update boss position and behavior"""
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
        """Boss takes damage"""
        self.health -= amount
        return self.health <= 0
    
    def is_defeated(self):
        """Check if boss is defeated"""
        return self.health <= 0
    
    def get_health_percentage(self):
        """Get health as a percentage"""
        return max(0, (self.health / self.max_health) * 100)
    
    def draw(self, surface):
        """Draw boss on screen"""
        surface.blit(self.image, self.rect)
        
        # Draw health bar
        bar_width = 100
        bar_height = 8
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 20
        
        # Background bar
        pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Health bar
        health_width = int(bar_width * self.get_health_percentage() / 100)
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
