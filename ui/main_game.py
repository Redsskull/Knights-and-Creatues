"""
Basic Pygame window setup for Knights and Creatures game
Sets up a basic Pygame window with title and event loop
"""

import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Knights and Creatures - Adventure Game")

    # Set up clock for controlling frame rate
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Fill the screen with a background color
        screen.fill((30, 30, 50))  # Dark blue-gray background

        # Update the display
        pygame.display.flip()

        # Control frame rate
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
