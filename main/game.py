import pygame
import settings
import math
from player import Player

class Camera():
    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0

    def update_camera(self, player_x, player_y):
        self.camera_x = player_x - (settings.WINDOW_WIDTH // 2)
        self.camera_y = player_y - (settings.WINDOW_HEIGHT // 2)

class RunResult: # this is to check whether the level was completed
    def __init__(self, score, completed):
        self.score = score
        self.completed = completed

def main(player):
    pygame.init()


    window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption("cis350 incremental platformer")
    clock = pygame.time.Clock()

    # Camera
    camera = Camera()

    tile_size = 50 # each tile is 50 pixels

    COIN_VALUE = 10
    COIN_COLOR = (255,215,0)
    PORTAL_COLOR = (160,60,220)

    #0=empty,1=solid,2=coin,3=exit portal
    level = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
        [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1],
        [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]


    # convert solid tiles into rectangles
    platforms = []
    coins = []
    portals = []

    score = 0
    score_font = pygame.font.Font(None, 28)

    end_time = pygame.time.get_ticks() + 20_000 # Change the number to change how long it takes for time to run out
    time_font = pygame.font.Font(None, 28)

    for row in range(len(level)):
        for column in range(len(level[row])):
            tile = pygame.Rect(column * tile_size, row * tile_size, tile_size, tile_size)

            if level[row][column] == 1:
                platforms.append(tile)
            elif level[row][column] == 2:
                coins.append(tile)
            elif level[row][column] == 3:
                portals.append(tile)

    # standard game logic
    running = True
    while running:
        dt = min(clock.tick(settings.FPS) / 1000, 0.05)
        camera.update_camera(player.player.x, player.player.y)

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

                if event.key == pygame.K_ESCAPE:
                    running = False

        # horiz movement
        # keeps track of the horizontal direction while dashing
        if player.dash_time > 0 and player.can_dash:
            player.dash(direction_x, dt)
        # normal horizontal movement when not dashing
        else:
            player.position.x += direction_x * player.speed * dt
        player.player.x = round(player.position.x)

        # removes jump when the player is falling
        if player.vertical_velocity > 0 and player.jumps == player.max_jumps:
            player.jumps -= 1

        # checks for collisions and applies gravity
        player.horizontal_collision(platforms)
        player.apply_gravity(dt)
        player.vertical_collision(platforms)

        # remove collected coins so eaach awards points only once per run
        for coin in coins[:]:
            if player.player.colliderect(coin):
                coins.remove(coin)
                score += COIN_VALUE

        for portal in portals:
            if player.player.colliderect(portal):
                return RunResult((score + 20), True) # Reach the portal and get 20 extra points, in the future implement bonuses on distance

        # draw the map and player
        window.fill(settings.BACKGROUND)

        for coin in coins:
            screen_coin = coin.move(-camera.camera_x, -camera.camera_y)
            pygame.draw.rect(window, COIN_COLOR, screen_coin)
        
        for portal in portals:
            screen_portal = portal.move(-camera.camera_x, -camera.camera_y)
            pygame.draw.rect(window, PORTAL_COLOR, screen_portal)
            
        for platform in platforms:
            screen_rect = platform.move(-camera.camera_x, -camera.camera_y)
            pygame.draw.rect(window, (0,0,0), screen_rect)

        player_screen_rect = player.player.move((-camera.camera_x), (-camera.camera_y))
        pygame.draw.rect(window, (50,100,255), player_screen_rect)

        score_text = score_font.render(f"Score: {score}", True, ("#b68f40"))
        window.blit(score_text, (10,10))

        left_ms = max(0, end_time - pygame.time.get_ticks())
        seconds = (left_ms + 999) // 1000
        if left_ms == 0:
            return RunResult(score, True)
        else:
            time = seconds

        time_text = time_font.render(f"Time: {time}", True,("#b68f40"))
        window.blit(time_text, (10,30))
        pygame.display.flip()

    return RunResult(score, False)

if __name__ == "__main__":
    player = Player(pygame.Rect(75, 1100, 30, 30))
    main(player)

