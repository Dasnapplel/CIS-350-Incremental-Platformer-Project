
import pygame
import settings


class Upgrade:
    def __init__(self, points):
        self.points = points
        self.upgrades = [["Double Jump", 100, False], ["Dash", 1000, False], ["Extra Time", 50, False], ["Speed Boost", 20, False]]
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
            window.blit(pygame.font.Font(None, 36).render(f"{upgrade[0]} - {upgrade[1]}", True, (0,0,0)), (self.upgrades_rects[i].x + 10, self.upgrades_rects[i].y + 5))
            window.blit(pygame.font.Font(None, 36).render(f"Purchased: {upgrade[2]}", True, (0,0,0)), (self.upgrades_rects[i].x + 10, self.upgrades_rects[i].y + 40))
            x_offset += 400
            if y_count % 2 == 1:
                y_offset += 100
            y_count += 1

    def on_click(self):
        # checks for clicks on the upgrade buttons and purchases if possible
        for i, upgrade in enumerate(self.upgrades):
            if self.upgrades_rects[i].collidepoint(pygame.mouse.get_pos()):
                if not upgrade[2] and self.points >= upgrade[1]:
                    self.points -= upgrade[1]
                    self.upgrades[i][2] = True

if __name__ == "__main__":
    pygame.init()
    upgrade = Upgrade(100000)
    window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                upgrade.on_click()

        window.fill(settings.BACKGROUND)
        upgrade.draw_upgrades(window)
        pygame.display.flip()

    pygame.quit()