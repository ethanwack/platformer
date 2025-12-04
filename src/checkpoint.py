import pygame
import os

class Checkpoint(pygame.sprite.Sprite):
    """Animated checkpoint flag using sprite sheet.

    Expects a sprite sheet named like 'Checkpoint (Flag Idle)(64x64).png' which is
    N frames horizontally with height 64.
    """
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.frames = self._load_sheet("Checkpoint (Flag Idle)(64x64).png", (64, 64)) or []
        self.out_frames = self._load_sheet("Checkpoint (Flag Out) (64x64).png", (64, 64)) or []
        self.frame = 0
        self.speed = 0.12
        self.activated = False
        self.image = self.frames[0] if self.frames else pygame.Surface((32, 64), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

    def _load_sheet(self, filename, frame_size):
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

    def activate(self):
        self.activated = True
        self.frame = 0

    def update(self):
        if self.activated and self.out_frames:
            self.frame += self.speed
            if int(self.frame) < len(self.out_frames):
                self.image = self.out_frames[int(self.frame)]
        elif self.frames:
            self.frame += self.speed
            self.image = self.frames[int(self.frame) % len(self.frames)]

    def draw(self, surface, camera_offset=0):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_offset
        surface.blit(self.image, draw_rect)
