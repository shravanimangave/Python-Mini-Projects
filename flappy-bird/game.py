import pygame

import settings as cfg
from entities.bird import Bird
from entities.pipe import PipePair
from utils.assets import get_fitted_image
from utils.collisions import bird_hit_bounds, update_pipe_collisions_and_score


def reset_game(assets):
    return {
        "bird": Bird(assets["bird"]),
        "pipes": [],
        "score": 0,
        "game_over": False,
        "started": False,
        "last_pipe_time": pygame.time.get_ticks(),
        "assets": assets,
    }


def handle_flap(game):
    if game["game_over"]:
        game.update(reset_game(game["assets"]))
        return

    game["started"] = True
    game["bird"].flap()


def update_game(game):
    if not game["started"] or game["game_over"]:
        return

    bird = game["bird"]
    pipes = game["pipes"]
    now = pygame.time.get_ticks()

    bird.update()

    if now - game["last_pipe_time"] >= cfg.PIPE_INTERVAL_MS:
        pipes.append(
            PipePair(
                cfg.WIDTH + cfg.PIPE_WIDTH,
                game["assets"]["pillar"],
                get_fitted_image,
            )
        )
        game["last_pipe_time"] = now

    for pipe in pipes:
        pipe.update()

    score_gain, hit_pipe = update_pipe_collisions_and_score(bird, pipes)
    game["score"] += score_gain
    if hit_pipe:
        game["game_over"] = True

    game["pipes"] = [pipe for pipe in pipes if not pipe.is_off_screen()]

    if bird_hit_bounds(bird):
        game["game_over"] = True
