"""
Game constants and configuration
"""

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# World dimensions (for side-scrolling)
WORLD_WIDTH = 3000  # Much wider for exploration

# Game settings
FPS = 60

# Difficulty settings
DIFFICULTY_SETTINGS = {
    "EASY": {
        "GRAVITY": 0.4,
        "PLAYER_SPEED": 6,
        "JUMP_POWER": 11,
        "ENEMY_SPEED": 1.5,
        "ENEMY_DAMAGE": False  # Enemies can't hurt you
    },
    "MEDIUM": {
        "GRAVITY": 0.5,
        "PLAYER_SPEED": 5,
        "JUMP_POWER": 10,
        "ENEMY_SPEED": 2,
        "ENEMY_DAMAGE": True
    },
    "HARD": {
        "GRAVITY": 0.6,
        "PLAYER_SPEED": 4,
        "JUMP_POWER": 9,
        "ENEMY_SPEED": 3,
        "ENEMY_DAMAGE": True
    }
}

# Default settings
GRAVITY = 0.5
PLAYER_SPEED = 5
JUMP_POWER = 10
ENEMY_SPEED = 2

# Colors
COLOR_PLATFORM = (100, 200, 100)
COLOR_PLAYER = (255, 0, 0)
COLOR_ENEMY = (255, 100, 100)
COLOR_GOAL = (255, 215, 0)
COLOR_BACKGROUND = (135, 206, 235)
COLOR_LIGHT_PLATFORM = (150, 220, 150)

# Font
FONT_SIZE_SMALL = 24
FONT_SIZE_MEDIUM = 36
FONT_SIZE_LARGE = 48
