import pygame

import settings as cfg


class Bird:
    def __init__(self, images):
        self.images = images
        self.x = cfg.BIRD_X
        self.y = cfg.HEIGHT // 2
        self.velocity = 0
        self.animation_index = 0
        self.last_animation_time = pygame.time.get_ticks()
        self.dead = False

    @property
    def rect(self):
        return pygame.Rect(
            self.x - cfg.BIRD_COLLISION_WIDTH // 2,
            int(self.y) - cfg.BIRD_COLLISION_HEIGHT // 2,
            cfg.BIRD_COLLISION_WIDTH,
            cfg.BIRD_COLLISION_HEIGHT,
        )

    def flap(self):
        if self.dead:
            return
        self.velocity = cfg.BIRD_FLAP_STRENGTH

    def kill(self):
        self.dead = True

    def update(self, animate=True):
        self.velocity = min(
            self.velocity + cfg.BIRD_GRAVITY,
            cfg.BIRD_MAX_FALL_SPEED,
        )
        self.y += self.velocity
        if animate and not self.dead:
            now = pygame.time.get_ticks()
            if now - self.last_animation_time >= cfg.BIRD_ANIMATION_MS:
                self.animation_index = (self.animation_index + 1) % 3
                self.last_animation_time = now

    def get_image(self):
        if self.dead:
            return self.images["dead"]
        frames = ("flap_up", "flap_mid", "flap_down")
        return self.images[frames[self.animation_index]]

    def draw(self, surface):
        image = self.get_image()
        rect = image.get_rect(center=(self.x, int(self.y)))
        surface.blit(image, rect)
