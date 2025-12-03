"""
Platform class - represents static platforms in the level
"""
import pygame
from src.constants import COLOR_PLATFORM

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(COLOR_PLATFORM)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self, surface):
        """Draw platform on screen"""
        surface.blit(self.image, self.rect)
