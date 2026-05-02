import random

import pygame

import settings as cfg
from utils.assets import get_scaled_image


class PipePair:
    def __init__(self, x, images, fit_image):
        top_height = random.randint(cfg.MIN_PIPE_HEIGHT, cfg.MAX_PIPE_TOP_HEIGHT)

        self.x = x
        self.images = images
        self.fit_image = fit_image
        self.top_rect = pygame.Rect(x, 0, cfg.PIPE_WIDTH, top_height)
        self.bottom_rect = pygame.Rect(
            x,
            top_height + cfg.PIPE_GAP,
            cfg.PIPE_WIDTH,
            cfg.PLAYABLE_HEIGHT - top_height - cfg.PIPE_GAP,
        )
        self.scored = False

    def update(self):
        self.x -= cfg.PIPE_SPEED
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def is_off_screen(self):
        return (
            self.get_pillar_draw_rect(self.top_rect).right < 0
            and self.get_pillar_draw_rect(self.bottom_rect).right < 0
        )

    def collides_with(self, rect):
        return self.top_collision_rect.colliderect(rect) or self.bottom_collision_rect.colliderect(rect)

    @property
    def top_collision_rect(self):
        return self.top_rect.inflate(
            -cfg.PIPE_COLLISION_INSET_X * 2,
            -cfg.PIPE_COLLISION_INSET_Y * 2,
        )

    @property
    def bottom_collision_rect(self):
        return self.bottom_rect.inflate(
            -cfg.PIPE_COLLISION_INSET_X * 2,
            -cfg.PIPE_COLLISION_INSET_Y * 2,
        )

    def get_pillar_image(self, height):
        if height < cfg.PILLAR_SMALL_MAX_HEIGHT:
            return self.images["small"]
        if height < cfg.PILLAR_MID_MAX_HEIGHT:
            return self.images["mid"]
        return self.images["tall"]

    def get_pillar_draw_rect(self, pipe_rect):
        visual_width = max(cfg.PIPE_WIDTH, cfg.PILLAR_VISUAL_WIDTH)
        return pygame.Rect(
            pipe_rect.centerx - visual_width // 2,
            pipe_rect.y,
            visual_width,
            pipe_rect.height,
        )

    def draw(self, surface):
        top_image = self.get_pillar_image(self.top_rect.height)
        bottom_image = self.get_pillar_image(self.bottom_rect.height)
        top_draw_rect = self.get_pillar_draw_rect(self.top_rect)
        bottom_draw_rect = self.get_pillar_draw_rect(self.bottom_rect)
        surface.blit(
            get_scaled_image(
                top_image,
                top_draw_rect.size,
                flip_y=True,
            ),
            top_draw_rect,
        )
        surface.blit(
            get_scaled_image(
                bottom_image,
                bottom_draw_rect.size,
            ),
            bottom_draw_rect,
        )
