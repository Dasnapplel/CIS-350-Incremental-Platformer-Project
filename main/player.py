import pygame
import math

class Player():
    def __init__(self, player):
        self.player = player
        self.position = pygame.Vector2(player.topleft)
        print(f"Player initialized at position: {self.position}")
        self.direction_x = 0

        self.speed = 250
        self.gravity = 1200
        self.jump_speed = 550
        self.max_fall_speed = 800

        self.can_dash = False
        self.dash_cooldown = 0
        self.dash_time = 0  # duration of the dash in seconds
        self.dash_speed = 2 * self.speed  # speed during the dash
        self.dash_offset = 0
            
        self.max_jumps = 1
        self.jumps = 0

        self.vertical_velocity = 0

    def get_inputs(self):
        keys = pygame.key.get_pressed()
        self.direction_x = (
                        int(keys[pygame.K_d] or keys[pygame.K_RIGHT])
                        - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
                    )


    def jump(self):
        self.vertical_velocity = -self.jump_speed
        self.jumps -= 1
        print("Jumped!")

    def dash(self, x, dt):
        self.dash_offset = x * self.dash_speed * dt
        self.position.x += self.dash_offset
        self.dash_time -= dt
        self.vertical_velocity = 0

    def direction(self):
        # Calculates the movement value of the direction the character is currently facing.
        keys = pygame.key.get_pressed()

        faced_direction = (
                        int(keys[pygame.K_d] or keys[pygame.K_RIGHT])
                        - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
                    )
        self.direction_x = faced_direction

    def apply_gravity(self, dt):
        self.vertical_velocity += self.gravity * dt
        self.vertical_velocity = min(self.vertical_velocity, self.max_fall_speed)
        
        self.position.y += self.vertical_velocity * dt
        
        self.player.y = math.ceil(self.position.y)

    def horizontal_collision(self, platforms):
        for platform in platforms:
            if self.player.colliderect(platform):
                if self.direction_x > 0:
                    self.player.right = platform.left
                elif self.direction_x < 0:
                    self.player.left = platform.right

                self.position.x = self.player.x

    def vertical_collision(self, platforms):
        for platform in platforms:
            if self.player.colliderect(platform):
                if self.vertical_velocity > 0:
                    # landing on top of a tile
                    self.player.bottom = platform.top
                    self.jumps = self.max_jumps
                elif self.vertical_velocity < 0:
                    # hitting the underside of a tile
                    self.player.top = platform.bottom

                self.position.y = self.player.y
                self.vertical_velocity = 0

    def update(self):
        return 0