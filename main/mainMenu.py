import os
import sys
import pygame
from PIL import Image, ImageSequence
import game
import upgrades

from button import Button
import settings

pygame.init()

# Setup paths relative to this script file so it runs reliably from anywhere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def load_gif_frames(filepath, target_size=None):
    """Load all frames of an animated GIF and convert them to Pygame surfaces."""
    pil_img = Image.open(filepath)
    frames = []
    durations = []

    for frame in ImageSequence.Iterator(pil_img):
        # Convert frame to RGBA format for Pygame
        frame_rgba = frame.convert("RGBA")
        surface = pygame.image.fromstring(
            frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
        ).convert_alpha()

        if target_size:
            surface = pygame.transform.scale(surface, target_size)

        frames.append(surface)
        durations.append(frame.info.get("duration", 100))

    return frames, durations


def get_font(size):
    """Helper to return a Pygame font object of given size."""
    return pygame.font.Font(None, size)


def main_menu(upgrade_shop):
    pygame.display.set_caption("Menu")
    window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Load GIF background frames scaled to window size
    gif_path = os.path.join(ASSETS_DIR, "neon_city_title_screen_loop.gif")
    bg_frames, bg_durations = load_gif_frames(
        gif_path, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
    )
    frame_duration = bg_durations[0] if bg_durations and bg_durations[0] > 0 else 100

    center_x = settings.WINDOW_WIDTH // 2

    # Title text
    menu_font = get_font(100)
    MENU_TEXT = menu_font.render("NEOPTIMIZER", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(center_x, 100))

    # Load button images once outside the loop for performance
    # Note: assets/upgradesButton.svg has 'Start Run' graphic, assets/PlayButton.svg has 'Upgrades' graphic
    play_img = pygame.image.load(os.path.join(ASSETS_DIR, "upgradesButton.svg"))
    upgrades_img = pygame.image.load(os.path.join(ASSETS_DIR, "PlayButton.svg"))

    btn_font = get_font(30)
    PLAY_BUTTON = Button(
        image=play_img,
        pos=(center_x, 260),
        text_input="",
        font=btn_font,
        base_color="yellow",
        hovering_color="white",
    )
    UPGRADES_BUTTON = Button(
        image=upgrades_img,
        pos=(center_x, 400),
        text_input="",
        font=btn_font,
        base_color="yellow",
        hovering_color="white",
    )

    while True:
        # Calculate current GIF frame based on elapsed time
        current_time = pygame.time.get_ticks()
        frame_index = (current_time // frame_duration) % len(bg_frames)
        window.blit(bg_frames[frame_index], (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        window.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, UPGRADES_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    result = game.main()
                    upgrade_shop.points += result.score
                    if result.completed:
                        upgrades.upgrade_shop_main(upgrade_shop)

                if UPGRADES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    upgrades.upgrade_shop_main(upgrade_shop)

        pygame.display.update()
        clock.tick(settings.FPS)


if __name__ == "__main__":
    upgrade_shop = upgrades.UpgradeWindow(0)
    main_menu(upgrade_shop)
