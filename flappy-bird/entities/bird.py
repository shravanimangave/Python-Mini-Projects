import pygame

import settings as cfg


class Bird:
    def __init__(self, images):
        self.images = images
        self.x = cfg.BIRD_X
        self.y = cfg.HEIGHT // 2
        self.velocity = 0

    @property
    def rect(self):
        return pygame.Rect(
            self.x - cfg.BIRD_COLLISION_WIDTH // 2,
            int(self.y) - cfg.BIRD_COLLISION_HEIGHT // 2,
            cfg.BIRD_COLLISION_WIDTH,
            cfg.BIRD_COLLISION_HEIGHT,
        )

    def flap(self):
        self.velocity = cfg.BIRD_FLAP_STRENGTH

    def update(self):
        self.velocity = min(
            self.velocity + cfg.BIRD_GRAVITY,
            cfg.BIRD_MAX_FALL_SPEED,
        )
        self.y += self.velocity

    def get_image(self, started, game_over):
        if game_over:
            return self.images["dead"]
        if not started:
            return self.images["flap_mid"]
        if self.velocity < cfg.BIRD_FLAP_UP_VELOCITY:
            return self.images["flap_up"]
        if self.velocity < cfg.BIRD_FLAP_MID_VELOCITY:
            return self.images["flap_mid"]
        if self.velocity < cfg.BIRD_FLAP_DOWN_VELOCITY:
            return self.images["flap_down"]
        if self.velocity < cfg.BIRD_FALLING_VELOCITY:
            return self.images["falling"]
        return self.images["falling_deep"]

    def draw(self, surface, started, game_over):
        image = self.get_image(started, game_over)
        rect = image.get_rect(center=(self.x, int(self.y)))
        surface.blit(image, rect)
