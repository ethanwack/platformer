"""
Main Game class that handles the game loop and state
"""
import pygame
from src.player import Player
from src.level import Level
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WORLD_WIDTH,
    DIFFICULTY_SETTINGS, COLOR_BACKGROUND,
    FONT_SIZE_SMALL, FONT_SIZE_MEDIUM
)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer - Mario-like Game")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.running = True
        self.game_state = "DIFFICULTY_SELECT"
        self.difficulty = None
        self.level = None
        self.player = None
        self.camera_x = 0  # Camera position for side-scrolling
        
    def start_game(self, difficulty):
        """Initialize game with selected difficulty"""
        self.difficulty = difficulty
        self.level = Level(difficulty)
        self.player = Player(64, 300, difficulty)
        self.camera_x = 0
        self.game_state = "PLAYING"
    
    def update_camera(self):
        """Update camera to follow player"""
        # Keep player roughly centered on screen (1/3 from left)
        target_x = self.player.rect.centerx - SCREEN_WIDTH // 3
        
        # Smooth camera movement
        self.camera_x = max(0, min(target_x, WORLD_WIDTH - SCREEN_WIDTH))
        
        # Update player and all objects based on camera position
        self.level.set_camera_offset(self.camera_x)
    
    def draw_difficulty_menu(self):
        """Draw difficulty selection menu"""
        self.screen.fill(COLOR_BACKGROUND)
        
        title = self.font_medium.render("SELECT DIFFICULTY", True, (0, 0, 0))
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        difficulties = ["EASY", "MEDIUM", "HARD"]
        button_y = 250
        button_height = 60
        button_width = 200
        
        mouse_pos = pygame.mouse.get_pos()
        
        for i, diff in enumerate(difficulties):
            button_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                button_y + i * (button_height + 20),
                button_width,
                button_height
            )
            
            # Highlight if mouse is over
            is_hovered = button_rect.collidepoint(mouse_pos)
            color = (100, 150, 255) if is_hovered else (100, 100, 100)
            
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
            
            text = self.font_small.render(diff, True, (255, 255, 255))
            self.screen.blit(text, (button_rect.centerx - text.get_width() // 2,
                                     button_rect.centery - text.get_height() // 2))
        
        pygame.display.flip()
        return difficulties, button_y, button_height, button_width
        
    def handle_events(self):
        """Handle user input and events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.game_state == "DIFFICULTY_SELECT":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    difficulties, button_y, button_height, button_width = self.draw_difficulty_menu()
                    mouse_pos = event.pos
                    
                    for i, diff in enumerate(difficulties):
                        button_rect = pygame.Rect(
                            SCREEN_WIDTH // 2 - button_width // 2,
                            button_y + i * (button_height + 20),
                            button_width,
                            button_height
                        )
                        if button_rect.collidepoint(mouse_pos):
                            self.start_game(diff)
                            break
            
            elif self.game_state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_r:
                        self.player.reset()
        
        # Continuous key checking for movement
        if self.game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move_right()
    
    def update(self):
        """Update game state"""
        if self.game_state != "PLAYING":
            return
        
        self.player.update()
        self.level.update()
        
        # Update boss
        if self.level.boss:
            self.level.boss.update()
        
        # Update camera
        self.update_camera()
        
        # Check collisions
        self.check_collisions()
        
        # Check if player fell off the map
        if self.player.rect.top > SCREEN_HEIGHT:
            self.player.reset()
    
    def check_collisions(self):
        """Check collisions between player and level elements"""
        # Check collision with platforms
        for platform in self.level.platforms:
            self.player.check_collision(platform)
        
        # Check collision with enemies
        for enemy in self.level.enemies:
            if self.player.rect.colliderect(enemy.rect):
                if self.player.velocity_y > 0 and self.player.rect.bottom < enemy.rect.centery:
                    # Player jumped on enemy
                    enemy.kill()
                    self.player.velocity_y = -15
                else:
                    # Player hit by enemy
                    self.player.reset()
        
        # Check collision with boss
        if self.level.boss and not self.level.boss.is_defeated():
            if self.player.rect.colliderect(self.level.boss.rect):
                if self.player.velocity_y > 0 and self.player.rect.bottom < self.level.boss.rect.centery:
                    # Player jumped on boss
                    boss_defeated = self.level.boss.take_damage(1)
                    self.player.velocity_y = -15
                    if boss_defeated:
                        # Boss defeated!
                        pass
                else:
                    # Player hit by boss
                    self.player.reset()
        
        # Check collision with goal (only if boss is defeated or no boss)
        if self.level.goal and self.player.rect.colliderect(self.level.goal):
            if not self.level.boss or self.level.boss.is_defeated():
                if self.level.current_level < 5:
                    self.level.load_next_level()
                    self.player.reset()
                else:
                    # Game complete!
                    self.game_state = "GAME_COMPLETE"
    
    def draw(self):
        """Draw everything on screen"""
        if self.game_state == "DIFFICULTY_SELECT":
            self.draw_difficulty_menu()
        
        elif self.game_state == "PLAYING":
            self.screen.fill(COLOR_BACKGROUND)
            
            # Draw with camera offset
            self.level.draw(self.screen, camera_offset=self.camera_x)
            
            # Draw player with camera offset
            player_draw_x = self.player.rect.x - self.camera_x
            player_draw_rect = self.player.rect.copy()
            player_draw_rect.x = player_draw_x
            if 0 <= player_draw_x <= SCREEN_WIDTH + 50:
                self.screen.blit(self.player.image, player_draw_rect)
            
            # Draw UI (no camera offset)
            level_text = self.font_small.render(f"Level: {self.level.current_level}/5", True, (0, 0, 0))
            difficulty_text = self.font_small.render(f"Difficulty: {self.difficulty}", True, (0, 0, 0))
            camera_text = self.font_small.render(f"Pos: {self.player.rect.x//50}", True, (0, 0, 0))
            self.screen.blit(level_text, (10, 10))
            self.screen.blit(difficulty_text, (10, 40))
            self.screen.blit(camera_text, (10, 70))
            
            # Draw boss status if boss exists
            if self.level.boss:
                if self.level.boss.is_defeated():
                    boss_status = self.font_small.render("Boss Defeated! Find the goal!", True, (0, 200, 0))
                    self.screen.blit(boss_status, (SCREEN_WIDTH - 320, 10))
                else:
                    boss_hp = self.font_small.render(f"Boss HP: {self.level.boss.health}/{self.level.boss.max_health}", True, (200, 0, 0))
                    self.screen.blit(boss_hp, (SCREEN_WIDTH - 250, 10))
            
            pygame.display.flip()
        
        elif self.game_state == "GAME_COMPLETE":
            self.screen.fill(COLOR_BACKGROUND)
            
            title = self.font_medium.render("YOU WIN!", True, (0, 0, 0))
            restart_text = self.font_small.render("Click to play again", True, (0, 0, 0))
            
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 300))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.game_state = "DIFFICULTY_SELECT"
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
