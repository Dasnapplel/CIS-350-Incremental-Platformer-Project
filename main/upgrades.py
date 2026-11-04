
import pygame
import settings


class UpgradeWindow:
    def __init__(self, points):
        self.points = points
        self.upgrades = [Upgrade("Double Jump", 100, 1), Upgrade("Dash", 1000, 1), Upgrade("Extra Time", 50, 5), Upgrade("Speed Boost", 20, 5)]
        self.upgrades_rects = [pygame.Rect(0, 0, 250, 80) for _ in self.upgrades]

    def draw_upgrades(self, window):
        x_offset = 100
        y_offset = 50
        y_count = 0
        points = pygame.font.Font(None, 28).render(f"Points: {self.points}", True, (0,0,0))
        # renders the points in the top right of the screen
        window.blit(points, points.get_rect(topright=(window.get_width() - 10, 10)))
        # draws every upgrade in a grid
        for i, upgrade in enumerate(self.upgrades):
            # sets the position of the upgrade buttons
            self.upgrades_rects[i].x = x_offset % window.get_width()
            self.upgrades_rects[i].y = y_offset
            pygame.draw.rect(window, (200,200,200), self.upgrades_rects[i])
            # adds name and purchase status to the upgrade button
            window.blit(pygame.font.Font(None, 36).render(f"{upgrade.name} - {upgrade.cost}", True, (0,0,0)), (self.upgrades_rects[i].x + 10, self.upgrades_rects[i].y + 5))
            window.blit(pygame.font.Font(None, 36).render(f"Current Level: {upgrade.current_level}", True, (0,0,0)), (self.upgrades_rects[i].x + 10, self.upgrades_rects[i].y + 40))
            x_offset += 400
            if y_count % 2 == 1:
                y_offset += 100
            y_count += 1

    def purchase(self):
        # checks for clicks on the upgrade buttons and purchases if possible
        for i, upgrade in enumerate(self.upgrades):
            if self.upgrades_rects[i].collidepoint(pygame.mouse.get_pos()):
                if upgrade.current_level < upgrade.max_level and self.points >= upgrade.cost:
                    self.points -= upgrade.cost
                    upgrade.level_up()

class Upgrade:
    def __init__(self, name, cost, max_level):
        self.name = name
        self.cost = cost
        self.max_level = max_level
        self.current_level = 0

    def level_up(self):
        if self.current_level < self.max_level:
            self.current_level += 1

def main():
    pygame.init()
    upgrade = UpgradeWindow(100000)
    window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                upgrade.purchase()

        window.fill(settings.BACKGROUND)
        upgrade.draw_upgrades(window)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()