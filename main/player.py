import pygame

class Player():
    def __init__(self, player):
        self.player = player
        self.position = pygame.Vector2(player.topleft)

        self.speed = 250
        self.gravity = 1200
        self.jump_speed = 550
        self.max_fall_speed = 800
        
        self.dash_cooldown = 0
        self.dash_time = 0  # duration of the dash in seconds
        self.dash_speed = 2 * self.speed  # speed during the dash
        self.dash_offset = 0
            
        self.max_jumps = 2
        self.jumps = 0

        self.vertical_velocity = 0

    