"""
Enemy class - represents enemies that move around
"""
import pygame
from src.constants import COLOR_ENEMY, DIFFICULTY_SETTINGS

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width=32, height=32, speed=2, patrol_left=None, patrol_right=None, difficulty="MEDIUM"):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(COLOR_ENEMY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Get speed from difficulty settings if speed not explicitly provided
        if speed == 2:  # Default value
            settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["MEDIUM"])
            self.speed = settings["ENEMY_SPEED"]
        else:
            self.speed = speed
        
        self.direction = 1  # 1 for right, -1 for left
        self.patrol_left = patrol_left if patrol_left is not None else x - 100
        self.patrol_right = patrol_right if patrol_right is not None else x + 100
    
    def update(self):
        """Update enemy position"""
        self.rect.x += self.speed * self.direction
        
        # Turn around at patrol boundaries
        if self.rect.left <= self.patrol_left or self.rect.right >= self.patrol_right:
            self.direction *= -1
    
    def kill(self):
        """Remove enemy from game"""
        self.image.set_alpha(0)
        self.rect.x = -1000  # Move off screen
    
    def draw(self, surface):
        """Draw enemy on screen"""
        surface.blit(self.image, self.rect)
