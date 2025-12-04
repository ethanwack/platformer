import pygame
import os

class WeaponPickup(pygame.sprite.Sprite):
    """Simple weapon pickup (e.g., spiked ball)"""
    def __init__(self, x, y, filename="Spiked Ball.png", ammo=3):
        super().__init__()
        self.x = x
        self.y = y
        self.filename = filename
        self.image = self._load_image(filename) or pygame.Surface((28, 28), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.ammo = ammo

    def _load_image(self, filename):
        try:
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
            return pygame.image.load(path).convert_alpha()
        except Exception:
            return None

    def draw(self, surface, camera_offset=0):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_offset
        surface.blit(self.image, draw_rect)
