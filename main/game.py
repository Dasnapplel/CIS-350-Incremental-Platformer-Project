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
    # position = pygame.Vector2(player.topleft)

    #speed = 250
    #gravity = 1200
    #jump_speed = 550
    #max_fall_speed = 800
    #dash_cooldown = 0
    #dash_time = 0  # duration of the dash in seconds
    #dash_speed = 2 * speed  # speed during the dash
    #dash_offset = 0
    #max_jumps = 2
    #jumps = 0

    #vertical_velocity = 0

    # standard game logic
    running = True
    while running:
        dt = min(clock.tick(settings.FPS) / 1000, 0.05)
        player.dash_cooldown -= dt

        direction_x = player.direction()

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
        keys = pygame.key.get_pressed()
        # keeps track of the horizontal direction while dashing
        if player.dash_time > 0:
            #player.dash_offset = direction_x * player.dash_speed * dt
            #player.position.x += player.dash_offset
            #player.dash_time -= dt
            #player.vertical_velocity = 0

            player.dash(direction_x, dt)
        # normal horizontal movement when not dashing
        else:
            # direction_x = player.on_right()
            player.position.x += direction_x * player.speed * dt
            print(player.position.x)
        player.player.x = round(player.position.x)
        

        # check horiz collisions
        for platform in platforms:
            if player.player.colliderect(platform):
                if direction_x > 0:
                    player.player.right = platform.left # might mess things up
                elif direction_x < 0:
                    player.player.left = platform.right

                player.position.x = player.player.x

        # apply gravity
        player.vertical_velocity += player.gravity * dt
        player.vertical_velocity = min(player.vertical_velocity, player.max_fall_speed)

        player.position.y += player.vertical_velocity * dt
        print(player.position.y)
        player.player.y = math.ceil(player.position.y)
        if player.jumps == player.max_jumps:
            player.jumps -= 1

        # check vertical collisions
        for platform in platforms:
            if player.player.colliderect(platform):
                if player.vertical_velocity > 0:
                    # landing on top of a tile
                    player.player.bottom = platform.top
                    player.jumps = player.max_jumps
                elif player.vertical_velocity < 0:
                    # hitting the underside of a tile
                    player.player.top = platform.bottom

                player.position.y = player.player.y
                player.vertical_velocity = 0

        # draw the map and player
        window.fill(settings.BACKGROUND)

        for platform in platforms:
            pygame.draw.rect(window, (0,0,0), platform)

        pygame.draw.rect(window, (50,100,255), player.player)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()



