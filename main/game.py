import pygame
import settings
import math
from player import Player

def main():
    pygame.init()

    window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption("cis350 incremental platformer")
    clock = pygame.time.Clock()

    tile_size = 50 # each tile is 50 pixels

    level = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    # convert solid tiles into rectangles
    platforms = []

    for row in range(len(level)):
        for column in range(len(level[row])):
            if level[row][column] == 1:
                platform = pygame.Rect(column * tile_size, row * tile_size, tile_size, tile_size)
                platforms.append(platform)

    # player
    player = Player(pygame.Rect(75,500,30,30))

    # standard game logic
    running = True
    while running:
        dt = min(clock.tick(settings.FPS) / 1000, 0.05)
        player.dash_cooldown -= dt

        player.direction()
        direction_x = player.direction_x

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP) and player.jumps > 0:
                    player.jump()

                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT) and player.dash_cooldown <= 0 and direction_x != 0:
                    player.dash_cooldown = 0.5
                    player.dash_time = 0.2
                    print("Dashed!")

        # horiz movement
        # keeps track of the horizontal direction while dashing
        if player.dash_time > 0:
            player.dash(direction_x, dt)
        # normal horizontal movement when not dashing
        else:
            player.position.x += direction_x * player.speed * dt
        player.player.x = round(player.position.x)

        # checks for collisions and applies gravity
        player.horizontal_collision(platforms)
        player.apply_gravity(dt)
        player.vertical_collision(platforms)

        # removes jump when the player is falling
        if player.vertical_velocity > 0 and player.jumps == player.max_jumps:
            player.jumps -= 1
        
        # draw the map and player
        window.fill(settings.BACKGROUND)

        for platform in platforms:
            pygame.draw.rect(window, (0,0,0), platform)

        pygame.draw.rect(window, (50,100,255), player.player)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()



