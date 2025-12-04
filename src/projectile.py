"""
Projectile class - represents projectiles fired by ranged enemies
"""
import pygame
import os
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=1, speed=5):
        super().__init__()
        
        # Try to load sprite, fall back to circle
        self.image = self._load_image()
        if not self.image:
            self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 200, 0), (4, 4), 4)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.direction = direction
        self.speed = speed
        self.lifetime = 300  # Frames before projectile disappears
    
    def _load_image(self):
        """Try to load projectile sprite from file"""
        try:
            # Try different projectile image names
            for filename in ["fireball.png", "projectile.png", "shot.png"]:
                path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
                if os.path.exists(path):
                    return pygame.image.load(path).convert_alpha()
        except Exception:
            pass
        return None
    
    def update(self):
        """Update projectile position"""
        self.rect.x += self.speed * self.direction
        self.lifetime -= 1
        
        # Remove if off-screen or lifetime expired
        if self.lifetime <= 0 or self.rect.left > SCREEN_WIDTH + 200 or self.rect.right < -200:
            self.kill()
    
    def draw(self, surface, camera_offset=0):
        """Draw projectile on screen with camera offset"""
        draw_x = self.rect.x - camera_offset
        if -50 <= draw_x <= SCREEN_WIDTH + 50:
            surface.blit(self.image, (draw_x, self.rect.y))
