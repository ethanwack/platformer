"""
Level class - manages platforms, enemies, and level layout
"""
import pygame
from src.platform import Platform
from src.enemy import Enemy
from src.boss import Boss
from src.constants import COLOR_GOAL, SCREEN_HEIGHT, WORLD_WIDTH

class Level:
    def __init__(self, difficulty="MEDIUM"):
        self.platforms = []
        self.enemies = []
        self.boss = None
        self.goal = None
        self.checkpoints = []
        self.pickups = []
        self.effects = []
        self.current_level = 1
        self.difficulty = difficulty
        self.camera_offset = 0
        self.load_level(1)
    
    def set_camera_offset(self, offset):
        """Set the camera offset for rendering"""
        self.camera_offset = offset
    
    def load_level(self, level_num):
        """Load a specific level"""
        self.platforms.clear()
        self.enemies.clear()
        self.checkpoints.clear()
        self.pickups.clear()
        self.effects.clear()
        self.boss = None
        self.enemy_counter = 0  # Track enemy count for sprite variation
        
        if level_num == 1:
            self.load_level_1()
        elif level_num == 2:
            self.load_level_2()
        elif level_num == 3:
            self.load_level_3()
        elif level_num == 4:
            self.load_level_4()
        elif level_num == 5:
            self.load_level_5()
        else:
            self.load_level_1()
        
        self.current_level = level_num
    
    def load_level_1(self):
        """Level 1 - Maze with tunnels and vertical challenges"""
        # Ground platforms
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 40, 3000, 40))
        
        # Entrance section - safe passage
        self.platforms.append(Platform(100, 450, 150, 20))
        self.platforms.append(Platform(300, 400, 150, 20))
        self.platforms.append(Platform(500, 350, 100, 20))
        
        # Maze section 1 - vertical challenge
        self.platforms.append(Platform(700, 480, 80, 20))
        self.platforms.append(Platform(750, 400, 80, 20))
        self.platforms.append(Platform(800, 320, 80, 20))
        
        # Maze section 2 - horizontal maze
        self.platforms.append(Platform(950, 350, 120, 20))
        self.platforms.append(Platform(1150, 300, 100, 20))
        self.platforms.append(Platform(1300, 250, 100, 20))
        
        # Challenging gap section
        self.platforms.append(Platform(1500, 320, 70, 20))
        self.platforms.append(Platform(1650, 380, 70, 20))
        self.platforms.append(Platform(1800, 320, 70, 20))
        self.platforms.append(Platform(1950, 380, 70, 20))
        
        # Tower to boss
        self.platforms.append(Platform(2100, 450, 100, 20))
        self.platforms.append(Platform(2200, 350, 80, 20))
        self.platforms.append(Platform(2300, 250, 80, 20))
        self.platforms.append(Platform(2400, 150, 80, 20))
        
        # Enemies scattered throughout - mix of types for variety
        if self.difficulty != "EASY":
            self.enemies.append(Enemy(400, 350, patrol_left=300, patrol_right=600, difficulty=self.difficulty, 
                                     enemy_type=self.enemy_counter, ability_type=Enemy.MELEE))
            self.enemy_counter += 1
            self.enemies.append(Enemy(1000, 300, patrol_left=900, patrol_right=1200, difficulty=self.difficulty, 
                                     enemy_type=self.enemy_counter, ability_type=Enemy.RANGED))
            self.enemy_counter += 1
        if self.difficulty == "HARD":
            self.enemies.append(Enemy(1700, 300, patrol_left=1600, patrol_right=1900, difficulty=self.difficulty, 
                                     enemy_type=self.enemy_counter, ability_type=Enemy.CHARGER))
            self.enemy_counter += 1
        
        # Boss at the end (after maze completion)
        self.boss = Boss(2600, 300, level=1, difficulty=self.difficulty)
        
        # Goal after defeating boss
        self.goal = pygame.Rect(2700, 250, 40, 40)
        # Place a checkpoint near the mid maze
        from src.checkpoint import Checkpoint
        self.checkpoints.append(Checkpoint(600, SCREEN_HEIGHT - 104))
        # Place a weapon pickup
        from src.weapon import WeaponPickup
        self.pickups.append(WeaponPickup(520, 320, filename="Spiked Ball.png", ammo=3))
    
    def load_level_2(self):
        """Level 2 - Tighter jumps with intricate pathways"""
        # Ground
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 40, 3000, 40))
        
        # Opening - dual paths
        self.platforms.append(Platform(100, 480, 100, 20))
        self.platforms.append(Platform(100, 300, 100, 20))
        
        # Upper path
        self.platforms.append(Platform(250, 420, 80, 20))
        self.platforms.append(Platform(380, 360, 80, 20))
        self.platforms.append(Platform(500, 300, 80, 20))
        
        # Lower path (alternative)
        self.platforms.append(Platform(250, 480, 80, 20))
        self.platforms.append(Platform(380, 460, 80, 20))
        self.platforms.append(Platform(500, 440, 80, 20))
        
        # Converging path
        self.platforms.append(Platform(700, 380, 100, 20))
        
        # Spiral section
        self.platforms.append(Platform(900, 450, 90, 20))
        self.platforms.append(Platform(1000, 380, 90, 20))
        self.platforms.append(Platform(1100, 310, 90, 20))
        self.platforms.append(Platform(1200, 240, 90, 20))
        
        # Dangerous platforming
        self.platforms.append(Platform(1400, 350, 60, 20))
        self.platforms.append(Platform(1500, 300, 60, 20))
        self.platforms.append(Platform(1600, 350, 60, 20))
        self.platforms.append(Platform(1700, 400, 60, 20))
        
        # Final ascent
        self.platforms.append(Platform(1900, 350, 100, 20))
        self.platforms.append(Platform(2050, 280, 100, 20))
        self.platforms.append(Platform(2200, 200, 100, 20))
        
        # Boss area approach
        self.platforms.append(Platform(2350, 150, 80, 20))
        
        # Enemies throughout maze - varied types for difficulty
        enemy_count = 2 if self.difficulty == "EASY" else (4 if self.difficulty == "MEDIUM" else 5)
        positions = [
            (350, 350, 250, 450),
            (1050, 350, 950, 1200),
            (1550, 300, 1400, 1700),
            (2100, 300, 2000, 2250),
            (2300, 200, 2200, 2400)
        ]
        ability_types = [Enemy.MELEE, Enemy.RANGED, Enemy.CHARGER, Enemy.MELEE, Enemy.RANGED]
        for i in range(min(enemy_count, len(positions))):
            x, y, left, right = positions[i]
            self.enemies.append(Enemy(x, y, patrol_left=left, patrol_right=right, difficulty=self.difficulty, 
                                     enemy_type=self.enemy_counter, ability_type=ability_types[i]))
            self.enemy_counter += 1
        
        # Boss at end of maze
        self.boss = Boss(2600, 200, level=2, difficulty=self.difficulty)
        
        # Goal
        self.goal = pygame.Rect(2700, 150, 40, 40)
        from src.checkpoint import Checkpoint
        from src.weapon import WeaponPickup
        self.checkpoints.append(Checkpoint(900, SCREEN_HEIGHT - 104))
        self.pickups.append(WeaponPickup(1200, 260, filename="Spiked Ball.png", ammo=2))
    
    def load_level_3(self):
        """Level 3 - Complex maze with precision jumps"""
        # Ground
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 40, 3000, 40))
        
        # Narrow entrance corridor
        self.platforms.append(Platform(50, 480, 120, 20))
        self.platforms.append(Platform(200, 450, 80, 20))
        
        # First maze section - narrow platforms
        self.platforms.append(Platform(350, 400, 60, 20))
        self.platforms.append(Platform(450, 380, 60, 20))
        self.platforms.append(Platform(550, 360, 60, 20))
        self.platforms.append(Platform(650, 380, 60, 20))
        self.platforms.append(Platform(750, 400, 60, 20))
        
        # Vertical tower
        self.platforms.append(Platform(900, 480, 70, 20))
        self.platforms.append(Platform(900, 380, 70, 20))
        self.platforms.append(Platform(900, 280, 70, 20))
        self.platforms.append(Platform(900, 180, 70, 20))
        
        # Horizontal precision section
        self.platforms.append(Platform(1100, 300, 50, 20))
        self.platforms.append(Platform(1200, 320, 50, 20))
        self.platforms.append(Platform(1300, 300, 50, 20))
        self.platforms.append(Platform(1400, 320, 50, 20))
        self.platforms.append(Platform(1500, 300, 50, 20))
        
        # Floating platforms challenge
        self.platforms.append(Platform(1700, 350, 60, 20))
        self.platforms.append(Platform(1800, 280, 60, 20))
        self.platforms.append(Platform(1900, 340, 60, 20))
        self.platforms.append(Platform(2000, 260, 60, 20))
        
        # Downward path to boss
        self.platforms.append(Platform(2150, 400, 100, 20))
        self.platforms.append(Platform(2300, 380, 100, 20))
        self.platforms.append(Platform(2450, 360, 100, 20))
        
        # More enemies in complex maze - varied types
        enemy_count = 3 if self.difficulty == "EASY" else (5 if self.difficulty == "MEDIUM" else 6)
        positions = [
            (500, 350, 400, 600),
            (1200, 300, 1100, 1400),
            (1600, 280, 1500, 1800),
            (1850, 320, 1750, 2000),
            (2200, 350, 2100, 2400),
            (2350, 350, 2250, 2500)
        ]
        ability_types = [Enemy.RANGED, Enemy.CHARGER, Enemy.MELEE, Enemy.RANGED, Enemy.CHARGER, Enemy.MELEE]
        for i in range(min(enemy_count, len(positions))):
            x, y, left, right = positions[i]
            self.enemies.append(Enemy(x, y, patrol_left=left, patrol_right=right, difficulty=self.difficulty, 
                                     enemy_type=self.enemy_counter, ability_type=ability_types[i]))
            self.enemy_counter += 1
        
        # Boss at end
        self.boss = Boss(2700, 280, level=3, difficulty=self.difficulty)
        
        # Goal
        self.goal = pygame.Rect(2800, 230, 40, 40)
        from src.checkpoint import Checkpoint
        from src.weapon import WeaponPickup
        self.checkpoints.append(Checkpoint(1100, SCREEN_HEIGHT - 104))
        self.pickups.append(WeaponPickup(1600, 240, filename="Spiked Ball.png", ammo=2))
    
    def load_level_4(self):
        """Level 4 - Advanced maze with multiple routes"""
        # Ground
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 40, 3000, 40))
        
        # Starting platform
        self.platforms.append(Platform(0, 480, 150, 20))
        
        # Route A - Upper path
        self.platforms.append(Platform(200, 400, 100, 20))
        self.platforms.append(Platform(350, 320, 100, 20))
        self.platforms.append(Platform(500, 240, 100, 20))
        
        # Route B - Lower path
        self.platforms.append(Platform(200, 480, 100, 20))
        self.platforms.append(Platform(350, 460, 100, 20))
        self.platforms.append(Platform(500, 440, 100, 20))
        
        # Routes merge
        self.platforms.append(Platform(700, 350, 120, 20))
        
        # Twisting corridor
        self.platforms.append(Platform(900, 300, 80, 20))
        self.platforms.append(Platform(1000, 380, 80, 20))
        self.platforms.append(Platform(1100, 280, 80, 20))
        self.platforms.append(Platform(1200, 360, 80, 20))
        
        # Long horizontal section
        self.platforms.append(Platform(1400, 320, 200, 20))
        
        # Vertical climb
        self.platforms.append(Platform(1700, 480, 70, 20))
        self.platforms.append(Platform(1700, 380, 70, 20))
        self.platforms.append(Platform(1700, 280, 70, 20))
        self.platforms.append(Platform(1700, 180, 70, 20))
        
        # Final gauntlet
        self.platforms.append(Platform(1900, 300, 60, 20))
        self.platforms.append(Platform(2000, 350, 60, 20))
        self.platforms.append(Platform(2100, 300, 60, 20))
        self.platforms.append(Platform(2200, 350, 60, 20))
        
        # Boss approach
        self.platforms.append(Platform(2350, 250, 100, 20))
        self.platforms.append(Platform(2500, 200, 100, 20))
        
        # Many enemies - balanced mix
        enemy_count = 4 if self.difficulty == "EASY" else (6 if self.difficulty == "MEDIUM" else 7)
        positions = [
            (300, 350, 200, 400),
            (600, 350, 500, 750),
            (1050, 320, 950, 1200),
            (1400, 280, 1300, 1600),
            (1750, 350, 1650, 1900),
            (2050, 300, 1950, 2150),
            (2300, 280, 2200, 2500)
        ]
        ability_types = [Enemy.MELEE, Enemy.RANGED, Enemy.CHARGER, Enemy.MELEE, Enemy.RANGED, Enemy.CHARGER, Enemy.MELEE]
        for i in range(min(enemy_count, len(positions))):
            x, y, left, right = positions[i]
            self.enemies.append(Enemy(x, y, patrol_left=left, patrol_right=right, difficulty=self.difficulty, 
                                     enemy_type=self.enemy_counter, ability_type=ability_types[i]))
            self.enemy_counter += 1
        
        # Boss
        self.boss = Boss(2700, 200, level=4, difficulty=self.difficulty)
        
        # Goal
        self.goal = pygame.Rect(2800, 150, 40, 40)
        from src.checkpoint import Checkpoint
        from src.weapon import WeaponPickup
        self.checkpoints.append(Checkpoint(1400, SCREEN_HEIGHT - 104))
        self.pickups.append(WeaponPickup(1800, 320, filename="Spiked Ball.png", ammo=3))
    
    def load_level_5(self):
        """Level 5 - Expert maze leading to final boss"""
        # Ground
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 40, 3000, 40))
        
        # Entrance - narrow passage
        self.platforms.append(Platform(0, 500, 100, 20))
        self.platforms.append(Platform(50, 450, 80, 20))
        
        # Complex winding path
        self.platforms.append(Platform(150, 400, 70, 20))
        self.platforms.append(Platform(250, 450, 70, 20))
        self.platforms.append(Platform(350, 380, 70, 20))
        self.platforms.append(Platform(450, 440, 70, 20))
        self.platforms.append(Platform(550, 360, 70, 20))
        
        # Vertical sections
        self.platforms.append(Platform(700, 500, 60, 20))
        self.platforms.append(Platform(700, 380, 60, 20))
        self.platforms.append(Platform(700, 260, 60, 20))
        
        # Precision platforming
        self.platforms.append(Platform(850, 350, 50, 20))
        self.platforms.append(Platform(920, 300, 50, 20))
        self.platforms.append(Platform(990, 350, 50, 20))
        self.platforms.append(Platform(1060, 300, 50, 20))
        self.platforms.append(Platform(1130, 350, 50, 20))
        
        # Dangerous corridors
        self.platforms.append(Platform(1300, 320, 80, 20))
        self.platforms.append(Platform(1450, 380, 80, 20))
        self.platforms.append(Platform(1600, 300, 80, 20))
        self.platforms.append(Platform(1750, 360, 80, 20))
        
        # Tower climb
        self.platforms.append(Platform(1950, 480, 70, 20))
        self.platforms.append(Platform(1950, 360, 70, 20))
        self.platforms.append(Platform(1950, 240, 70, 20))
        self.platforms.append(Platform(1950, 120, 70, 20))
        
        # Final approach
        self.platforms.append(Platform(2150, 350, 80, 20))
        self.platforms.append(Platform(2300, 280, 80, 20))
        self.platforms.append(Platform(2450, 200, 80, 20))
        self.platforms.append(Platform(2600, 120, 80, 20))
        
        # Maximum enemies - all types used
        enemy_count = 5 if self.difficulty == "EASY" else (7 if self.difficulty == "MEDIUM" else 8)
        positions = [
            (200, 380, 100, 350),
            (450, 400, 350, 550),
            (700, 350, 600, 850),
            (1000, 300, 900, 1150),
            (1500, 330, 1350, 1750),
            (1950, 350, 1850, 2100),
            (2250, 300, 2150, 2400),
            (2500, 200, 2400, 2650)
        ]
        ability_types = [Enemy.CHARGER, Enemy.MELEE, Enemy.RANGED, Enemy.CHARGER, Enemy.MELEE, Enemy.RANGED, Enemy.CHARGER, Enemy.MELEE]
        for i in range(min(enemy_count, len(positions))):
            x, y, left, right = positions[i]
            self.enemies.append(Enemy(x, y, patrol_left=left, patrol_right=right, difficulty=self.difficulty, 
                                     enemy_type=self.enemy_counter, ability_type=ability_types[i]))
            self.enemy_counter += 1
        
        # FINAL BOSS - at far end of level
        self.boss = Boss(2800, 150, level=5, difficulty=self.difficulty)
        
        # Goal - only accessible after boss defeat
        self.goal = pygame.Rect(2900, 100, 40, 40)
        from src.checkpoint import Checkpoint
        from src.weapon import WeaponPickup
        self.checkpoints.append(Checkpoint(2000, SCREEN_HEIGHT - 104))
        # Final level includes a few collectibles (reuse WeaponPickup for now as chest)
        self.pickups.append(WeaponPickup(2300, 260, filename="Spiked Ball.png", ammo=5))
    
    def load_next_level(self):
        """Load the next level"""
        next_level = self.current_level + 1
        if next_level <= 5:
            self.load_level(next_level)
        else:
            self.load_level(1)
    
    def update(self):
        """Update all level elements"""
        for enemy in self.enemies:
            enemy.update()
        for cp in getattr(self, 'checkpoints', []):
            cp.update()
        # pickups are static but could be animated in future
        # update transient effects
        for e in list(getattr(self, 'effects', [])):
            e.update()
            if not e.active:
                try:
                    self.effects.remove(e)
                except ValueError:
                    pass
    
    def draw(self, surface, camera_offset=0):
        """Draw all level elements with camera offset"""
        # Always draw background
        surface.fill((135, 206, 235))
        
        # Draw platforms with camera offset
        for platform in self.platforms:
            draw_x = platform.rect.x - camera_offset
            
            # Always draw ground, otherwise check visibility
            if platform.rect.y >= SCREEN_HEIGHT - 50:  # Ground platform
                # Draw ground even if mostly off-screen
                if draw_x < 1100:  # At least partially on screen
                    platform_copy = platform.rect.copy()
                    platform_copy.x = draw_x
                    surface.blit(platform.image, platform_copy)
            elif -100 <= draw_x <= 1100:  # Other platforms only if visible
                platform_copy = platform.rect.copy()
                platform_copy.x = draw_x
                surface.blit(platform.image, platform_copy)
        
        # Draw enemies with camera offset
        for enemy in self.enemies:
            draw_x = enemy.rect.x - camera_offset
            if -50 <= draw_x <= 1050:
                enemy_copy = enemy.rect.copy()
                enemy_copy.x = draw_x
                surface.blit(enemy.image, enemy_copy)
            
            # Draw enemy projectiles
            for projectile in getattr(enemy, 'projectiles', []):
                projectile.draw(surface, camera_offset=camera_offset)

        # Draw pickups
        for p in getattr(self, 'pickups', []):
            p.draw(surface, camera_offset=camera_offset)

        # Draw checkpoints
        for cp in getattr(self, 'checkpoints', []):
            cp.update()
            cp.draw(surface, camera_offset=camera_offset)
        
        # Draw boss with camera offset
        if self.boss and not self.boss.is_defeated():
            draw_x = self.boss.rect.x - camera_offset
            if -100 <= draw_x <= 1100:
                boss_copy = self.boss.rect.copy()
                boss_copy.x = draw_x
                surface.blit(self.boss.image, boss_copy)
                
                # Draw boss health bar
                bar_width = 100
                bar_height = 8
                bar_x = boss_copy.centerx - bar_width // 2
                bar_y = boss_copy.top - 20
                
                import pygame
                # Background bar
                pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
                
                # Health bar
                health_width = int(bar_width * self.boss.get_health_percentage() / 100)
                pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))
                
                # Border
                pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw goal with camera offset
        if self.goal:
            draw_x = self.goal.x - camera_offset
            if -50 <= draw_x <= 1050:
                goal_copy = self.goal.copy()
                goal_copy.x = draw_x
                pygame.draw.rect(surface, COLOR_GOAL, goal_copy)
                # Draw a star or flag effect
                pygame.draw.circle(surface, (255, 255, 0), goal_copy.center, 10)
