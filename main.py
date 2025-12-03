"""
Platformer Game - Mario-like game built with Pygame
"""
import pygame
import sys
from src.game import Game

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create and run the game
    game = Game()
    game.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
