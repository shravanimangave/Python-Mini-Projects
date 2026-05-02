import pygame

import settings as cfg


class SilentSound:
    def play(self):
        pass


def load_sound(filename):
    if not pygame.mixer.get_init():
        return SilentSound()

    path = cfg.SOUND_DIR / filename
    try:
        sound = pygame.mixer.Sound(path)
    except pygame.error:
        return SilentSound()

    sound.set_volume(cfg.SOUND_VOLUME)
    return sound


def load_sounds():
    return {
        name: load_sound(filename)
        for name, filename in cfg.SOUNDS.items()
    }
