
import os

import pygame
import settings
import button

def get_asset_path(filename):
        return os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets"), filename)

class UpgradeWindow:
    def __init__(self, points):
        self.points = points
        self.background = pygame.transform.scale(pygame.image.load(get_asset_path("upgrade_shop.png")), (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.upgrades = [("Double Jump", 100, 1), ("Dash", 1000, 1), ("Extra Time", 50, 10), ("Speed Boost", 20, 5)]
        self.create_upgrade()
        self.back_button_image = pygame.transform.scale(pygame.image.load(get_asset_path("back.png")), (100,50))
        self.back_button = button.Button(self.back_button_image, (settings.WINDOW_WIDTH//2, settings.WINDOW_HEIGHT - 50), "", pygame.font.Font(None, 36), (0,0,0), (0,0,0))

    def draw_upgrades(self, window):
        # Draws the background image
        window.blit(self.background, (0, 0))
        # Labels the upgrade shop at the top of the window
        menu_text = pygame.font.Font(None, 36).render("Upgrade Shop", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(settings.WINDOW_WIDTH//2, 50))
        window.blit(menu_text, menu_rect)
        # Displays the player's points in the top right corner
        points = pygame.font.Font(None, 28).render(f"Points: {self.points}", True, (255,255,255))
        window.blit(points, points.get_rect(topright=(window.get_width() - 10, 10)))

        # draws every upgrade in a grid
        for upgrade in self.upgrades:
            upgrade.update(window)
            name = pygame.font.Font(None, 36).render(upgrade.name, True, (0,0,0))
            window.blit(name, name.get_rect(center=(upgrade.x_pos, upgrade.y_pos - 5)))
            upgrade.draw_tallies((upgrade.x_pos, upgrade.y_pos + 20), window)
            # Draws cost of the upgrade
            cost_text = pygame.font.Font(None, 22).render(f"{upgrade.cost}", True, (255, 215, 0))
            window.blit(cost_text, cost_text.get_rect(right = upgrade.rect.right -14, centery = upgrade.y_pos + 30))
            # Draws the back button
            self.back_button.update(window)
            

    def purchase(self, position):
        # checks for clicks on the upgrade buttons and purchases if possible
        for upgrade in self.upgrades:
            if upgrade.checkForInput(position):
                if upgrade.current_level < upgrade.max_level and self.points >= upgrade.cost:
                    self.points -= upgrade.cost
                    upgrade.level_up()

    def create_upgrade(self):
        for i, upgrade in enumerate(self.upgrades):
            self.upgrades[i] = Upgrade(((i%3+0.5)*round(settings.WINDOW_WIDTH/3), (i//3+1)*120), upgrade[0], upgrade[1], upgrade[2])

class Upgrade(button.Button):
    def __init__(self, pos, name, cost, max_level):
        self.image = pygame.image.load(get_asset_path("upgrade.png"))
        self.scale(1)
        super().__init__(self.image, pos, "", pygame.font.Font(None, 36), (200,200,200), (150,150,150))
        self.name = name
        self.cost = cost
        self.max_level = max_level
        self.current_level = 0

    def scale(self, scale):
        self.image = pygame.transform.scale(self.image, (200*scale, 100*scale))

    def level_up(self):
        if self.current_level < self.max_level:
            self.current_level += 1

    def draw_tallies(self, position, window):
        tally_height = 12
        tally_width = 6
        for i in range(self.max_level):
            tally = pygame.Rect(0, 0, tally_width, tally_height)
            # Calculates the center x of each tally based on the total number of tallies
            tally.centerx = (i+0.5)*(tally_width + tally_width//1.2) - (self.max_level*(tally_width + tally_width//1.2))//2 + position[0] 
            tally.y = position[1]
            if i < self.current_level:
                pygame.draw.rect(window, (255, 215, 0), tally)
            else:
                pygame.draw.rect(window, (150,150,150), tally)

def upgrade_shop_main(UpgradeWindow):
    pygame.init()
    upgrade_shop = UpgradeWindow
    window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                upgrade_shop.purchase(pygame.mouse.get_pos())
                if upgrade_shop.back_button.checkForInput(pygame.mouse.get_pos()):
                    running = False

        window.fill(settings.BACKGROUND)
        upgrade_shop.draw_upgrades(window)
        pygame.display.flip()

if __name__ == "__main__":
    upgrade_shop_main(UpgradeWindow(100000))
