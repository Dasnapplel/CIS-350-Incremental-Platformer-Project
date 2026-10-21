import pygame
import settings


def main():
    pygame.init()

    window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption("cis350 incremental platformer")
    clock = pygame.time.Clock()

    # a box that surrounds the player for testing
    box = pygame.Rect(50,50,700,500)
    border_width = 4
    inside = box.inflate(-border_width * 2, -border_width * 2)

    # player
    player = pygame.Rect(0,0,30,30)
    player.center = box.center
    position = pygame.Vector2(player.topleft)
    speed = 250 # pixels per second

    # standard game logic
    running = True
    while running:
        dt = min(clock.tick(settings.FPS) / 1000, 0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # movement logic
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(
            int(keys[pygame.K_d] or keys[pygame.K_RIGHT])
            - int(keys[pygame.K_a] or keys[pygame.K_LEFT]),
            int(keys[pygame.K_s] or keys[pygame.K_DOWN])
            - int(keys[pygame.K_w] or keys[pygame.K_UP]),
        )

        # normalize so 2 keys doesn't increase mov. speed ex:(a+s != 500)
        if direction.length_squared() > 0:
            direction = direction.normalize()

        position += direction * speed * dt

        # keep the entire player inside the test box
        position.x = max(inside.left, min(position.x, inside.right - player.width))
        position.y = max(inside.top, min(position.y, inside.bottom - player.height))
        player.topleft = (round(position.x), round(position.y))

        window.fill(settings.BACKGROUND)
        pygame.draw.rect(window, (0,0,0), box, border_width)
        pygame.draw.rect(window, (50,100,255), player)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()



