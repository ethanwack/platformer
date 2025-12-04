import pygame
import os

class HitEffect:
    """Transient hit effect using available hit images (hit.png).

    Construct with a position (x,y) and it will play for a short duration.
    """
    def __init__(self, x, y, filename="hit.png", duration=12):
        self.x = x
        self.y = y
        self.frames = self._load_frames(filename)
        self.duration = duration
        self.timer = 0
        self.active = True

    def _load_frames(self, filename):
        try:
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
            img = pygame.image.load(path).convert_alpha()
            # If single image, return single-frame list
            return [img]
        except Exception:
            return []

    def update(self):
        self.timer += 1
        if self.timer >= self.duration:
            self.active = False

    def draw(self, surface, camera_offset=0):
        if not self.frames:
            return
        frame = self.frames[0]
        rect = frame.get_rect(center=(self.x - camera_offset, self.y))
        surface.blit(frame, rect)
