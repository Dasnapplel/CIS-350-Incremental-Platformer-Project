import pygame, sys, random
# sys library includes things for the game to interface with OS

from pygame.locals import * # imported module w/ various functions used by pygame that can be helpful

import settings

pygame.init()

print("pygame.ver") # test

# Game Setup
fpsClock = pygame.time.Clock() # Controls speed of game later

WINDOW = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)) # Sets display size
pygame.display.set_caption('CIS350 Incremental Platformer')

# Main

def main():
    running = True

    # The main game loop

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit

        # Rendering
        WINDOW.fill(settings.BACKGROUND)
        pygame.display.update()

        fpsClock.tick(settings.FPS)

main()