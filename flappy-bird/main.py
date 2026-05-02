import sys

import pygame

import settings as cfg
from game import SkyDashGame
from utils.assets import load_assets
from utils.audio import load_sounds


def create_fonts():
    return {
        "large": pygame.font.Font(None, 64),
        "medium": pygame.font.Font(None, 42),
        "small": pygame.font.Font(None, 26),
    }


def main():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.display.set_caption(cfg.GAME_TITLE)
    screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    clock = pygame.time.Clock()

    assets = load_assets()
    sounds = load_sounds()
    fonts = create_fonts()
    game = SkyDashGame(assets, sounds, fonts)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)

        if game.request_quit:
            pygame.quit()
            sys.exit()

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(cfg.FPS)


if __name__ == "__main__":
    main()
