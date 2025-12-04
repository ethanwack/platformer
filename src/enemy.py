"""
Enemy class - represents enemies that move around with different types and abilities
"""
import pygame
import os
from src.constants import COLOR_ENEMY, DIFFICULTY_SETTINGS


class Enemy(pygame.sprite.Sprite):
    # Enemy type constants
    MELEE = "melee"
    RANGED = "ranged"
    CHARGER = "charger"
    
    # Type settings: attack range, cooldown, damage, speed modifier
    TYPE_SETTINGS = {
        MELEE: {
            "attack_range": 60,
            "attack_delay": 60,
            "attack_damage": 1,
            "speed_multiplier": 1.0,
            "color_offset": 0,  # Use sprites 0-6
        },
        RANGED: {
            "attack_range": 250,
            "attack_delay": 90,
            "attack_damage": 1,
            "speed_multiplier": 0.7,
            "color_offset": 7,  # Use sprites 7-13
        },
        CHARGER: {
            "attack_range": 100,
            "attack_delay": 120,
            "attack_damage": 2,
            "speed_multiplier": 1.5,
            "color_offset": 14,  # Use sprites 14-19
        },
    }
    
    def __init__(self, x, y, width=32, height=32, speed=2, patrol_left=None, patrol_right=None, 
                 difficulty="MEDIUM", enemy_type=0, ability_type=MELEE):
        super().__init__()
        
        # Enemy ability type
        if ability_type not in self.TYPE_SETTINGS:
            ability_type = self.MELEE
        self.ability_type = ability_type
        self.ability_settings = self.TYPE_SETTINGS[ability_type]
        
        # Try to load sprite from sheet, fall back to colored square
        self.sprite_sheet = self._load_sprite_sheet("20 Enemies.png")
        self.sprite_index = enemy_type % 20 if self.sprite_sheet else 0
        
        if self.sprite_sheet and len(self.sprite_sheet) > self.sprite_index:
            self.image = self.sprite_sheet[self.sprite_index]
            width = self.image.get_width()
            height = self.image.get_height()
        else:
            self.image = pygame.Surface((width, height))
            # Color based on ability type
            if ability_type == self.RANGED:
                self.image.fill((100, 150, 255))  # Blue
            elif ability_type == self.CHARGER:
                self.image.fill((255, 150, 50))  # Orange
            else:
                self.image.fill(COLOR_ENEMY)  # Red (default melee)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Get speed from difficulty settings and apply type multiplier
        if speed == 2:  # Default value
            settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["MEDIUM"])
            self.speed = settings["ENEMY_SPEED"] * self.ability_settings["speed_multiplier"]
        else:
            self.speed = speed * self.ability_settings["speed_multiplier"]
        
        self.direction = 1  # 1 for right, -1 for left
        self.patrol_left = patrol_left if patrol_left is not None else x - 100
        self.patrol_right = patrol_right if patrol_right is not None else x + 100
        
        # Detection and attack
        self.detection_range = 250  # How far away to detect player
        self.attack_range = self.ability_settings["attack_range"]
        self.attack_cooldown = 0
        self.attack_delay = self.ability_settings["attack_delay"]
        self.attack_damage = self.ability_settings["attack_damage"]
        self.is_attacking = False
        self.attack_duration = 30  # How long the attack animation lasts
        self.attack_timer = 0
        
        # For ranged enemies: projectiles
        self.projectiles = []
        
        # For charger enemies: charging state
        self.is_charging = False
        self.charge_timer = 0
        self.charge_duration = 30
    
    def _load_sprite_sheet(self, filename):
        """Load and parse enemy sprite sheet."""
        try:
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
            sheet = pygame.image.load(path).convert_alpha()
            # Try to extract 20 enemies (630x500 sheet, so roughly 63x250 per enemy)
            # The sheet appears to be arranged in 10 columns x 2 rows
            sprites = []
            frame_width = sheet.get_width() // 10  # 63 pixels
            frame_height = sheet.get_height() // 2   # 250 pixels
            
            for row in range(2):
                for col in range(10):
                    x = col * frame_width
                    y = row * frame_height
                    frame_surf = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                    frame_surf.blit(sheet, (0, 0), (x, y, frame_width, frame_height))
                    sprites.append(frame_surf)
            
            return sprites if sprites else None
        except Exception:
            return None
    
    def update(self):
        """Update enemy position"""
        # Handle charger ability: speed boost when charging
        current_speed = self.speed
        if self.is_charging:
            current_speed = self.speed * 2  # Double speed when charging
            self.charge_timer -= 1
            if self.charge_timer <= 0:
                self.is_charging = False
        
        self.rect.x += current_speed * self.direction
        
        # Turn around at patrol boundaries
        if self.rect.left <= self.patrol_left or self.rect.right >= self.patrol_right:
            self.direction *= -1
        
        # Flip sprite based on direction
        if self.direction == -1:
            self.image = pygame.transform.flip(self.sprite_sheet[self.sprite_index], True, False) if self.sprite_sheet else self.image
        else:
            self.image = self.sprite_sheet[self.sprite_index] if self.sprite_sheet else self.image
        
        # Update attack timing
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.is_attacking:
            self.attack_timer += 1
            if self.attack_timer >= self.attack_duration:
                self.is_attacking = False
                self.attack_timer = 0
    
    def detect_player(self, player):
        """Check if player is within detection range."""
        distance = abs(player.rect.centerx - self.rect.centerx)
        return distance < self.detection_range
    
    def attack(self):
        """Start attack animation/behavior based on enemy type."""
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_timer = 0
            self.attack_cooldown = self.attack_delay
            
            # Type-specific attack logic
            if self.ability_type == self.CHARGER:
                # Chargers start charging for a dash attack
                self.is_charging = True
                self.charge_timer = self.charge_duration
            elif self.ability_type == self.RANGED:
                # Ranged enemies fire projectiles
                self._fire_projectile()
    
    def _fire_projectile(self):
        """Fire a projectile at the player (for ranged enemies)."""
        from src.projectile import Projectile
        projectile = Projectile(
            self.rect.centerx,
            self.rect.centery,
            direction=self.direction,
            speed=4
        )
        self.projectiles.append(projectile)
    
    def get_attack_rect(self):
        """Return the rect for attack collision."""
        if not self.is_attacking:
            return None
        
        # Attack characteristics based on type
        if self.ability_type == self.CHARGER and self.is_charging:
            # Chargers have a wide dash attack
            attack_rect = self.rect.inflate(60, 40)
        else:
            # Melee has moderate range, ranged doesn't have physical attack
            if self.ability_type == self.RANGED:
                return None  # Ranged enemies attack via projectiles
            attack_rect = self.rect.inflate(20, 20)
        
        return attack_rect
    
    def kill(self):
        """Remove enemy from game"""
        if self.sprite_sheet:
            self.image.set_alpha(0)
        self.rect.x = -1000  # Move off screen
    
    def draw(self, surface):
        """Draw enemy on screen"""
        surface.blit(self.image, self.rect)
