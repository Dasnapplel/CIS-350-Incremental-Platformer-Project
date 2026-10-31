import pygame
import settings
import math


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
    player = pygame.Rect(75,500,30,30)
    position = pygame.Vector2(player.topleft)

    speed = 250
    gravity = 1200
    jump_speed = 550
    max_fall_speed = 800
    dash_cooldown = 0
    dash_time = 0  # duration of the dash in seconds
    dash_speed = 2 * speed  # speed during the dash
    dash_offset = 0
    max_jumps = 2
    jumps = 0

    vertical_velocity = 0

    # standard game logic
    running = True
    while running:
        dt = min(clock.tick(settings.FPS) / 1000, 0.05)
        dash_cooldown -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP) and jumps > 0:
                    vertical_velocity = -jump_speed
                    jumps -= 1

                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT) and dash_cooldown <= 0 and direction_x != 0:
                    dash_cooldown = 0.5
                    dash_time = 0.2

        # horiz movement
        keys = pygame.key.get_pressed()
        # keeps track of the horizontal direction while dashing
        if dash_time > 0:
            dash_offset = direction_x * dash_speed * dt
            position.x += dash_offset
            dash_time -= dt
            vertical_velocity = 0
        # normal horizontal movement when not dashing
        else:
            direction_x = (
                int(keys[pygame.K_d] or keys[pygame.K_RIGHT])
                - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
            )
            position.x += direction_x * speed * dt
        player.x = round(position.x)

        # check horiz collisions
        for platform in platforms:
            if player.colliderect(platform):
                if direction_x > 0:
                    player.right = platform.left
                elif direction_x < 0:
                    player.left = platform.right

                position.x = player.x

        # apply gravity
        vertical_velocity += gravity * dt
        vertical_velocity = min(vertical_velocity, max_fall_speed)

        position.y += vertical_velocity * dt
        player.y = math.ceil(position.y)
        if jumps == max_jumps:
            jumps -= 1

        # check vertical collisions
        for platform in platforms:
            if player.colliderect(platform):
                if vertical_velocity > 0:
                    # landing on top of a tile
                    player.bottom = platform.top
                    jumps = max_jumps
                elif vertical_velocity < 0:
                    # hitting the underside of a tile
                    player.top = platform.bottom

                position.y = player.y
                vertical_velocity = 0

        # draw the map and player
        window.fill(settings.BACKGROUND)

        for platform in platforms:
            pygame.draw.rect(window, (0,0,0), platform)

        pygame.draw.rect(window, (50,100,255), player)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()



