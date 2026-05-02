import sys

import pygame

import settings as cfg
from game import handle_flap, reset_game, update_game
from utils.assets import load_assets


def draw_text(surface, font, text, color, center):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    surface.blit(rendered, rect)


def draw_game(surface, fonts, game):
    surface.fill(cfg.SKY_COLOR)

    for pipe in game["pipes"]:
        pipe.draw(surface)

    ground_rect = pygame.Rect(0, cfg.PLAYABLE_HEIGHT, cfg.WIDTH, cfg.GROUND_HEIGHT)
    pygame.draw.rect(surface, cfg.GROUND_COLOR, ground_rect)
    pygame.draw.line(
        surface,
        cfg.GROUND_LINE_COLOR,
        (0, ground_rect.top),
        (cfg.WIDTH, ground_rect.top),
        4,
    )

    game["bird"].draw(surface, game["started"], game["game_over"])

    draw_text(surface, fonts["large"], str(game["score"]), (255, 255, 255), (cfg.WIDTH // 2, 70))

    if not game["started"]:
        draw_text(surface, fonts["medium"], "Press Space to flap", (255, 255, 255), (cfg.WIDTH // 2, 290))
        draw_text(surface, fonts["small"], "Avoid the pipes", (45, 80, 90), (cfg.WIDTH // 2, 330))

    if game["game_over"]:
        draw_text(surface, fonts["medium"], "Game Over", (255, 255, 255), (cfg.WIDTH // 2, 290))
        draw_text(surface, fonts["small"], "Press Space to restart", (45, 80, 90), (cfg.WIDTH // 2, 330))


def main():
    pygame.init()
    pygame.display.set_caption("Flappy Bird")
    screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    clock = pygame.time.Clock()
    assets = load_assets()
    fonts = {
        "large": pygame.font.Font(None, 72),
        "medium": pygame.font.Font(None, 42),
        "small": pygame.font.Font(None, 30),
    }
    game = reset_game(assets)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                handle_flap(game)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_flap(game)

        update_game(game)
        draw_game(screen, fonts, game)
        pygame.display.flip()
        clock.tick(cfg.FPS)


if __name__ == "__main__":
    main()
