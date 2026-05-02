import pygame
import numpy

import settings as cfg


SCALED_IMAGE_CACHE = {}


def remove_background(surface):
    surface = surface.copy().convert_alpha()
    rgb = pygame.surfarray.pixels3d(surface)
    alpha = pygame.surfarray.pixels_alpha(surface)
    background = numpy.array(cfg.IMAGE_BACKGROUND_COLOR, dtype=numpy.int16)
    diff = numpy.abs(rgb.astype(numpy.int16) - background)
    background_mask = numpy.all(diff <= cfg.IMAGE_BACKGROUND_TOLERANCE, axis=2)
    alpha[background_mask] = 0
    del rgb
    del alpha
    return surface


def crop_transparent_padding(surface):
    rect = surface.get_bounding_rect(min_alpha=1)
    if rect.width == 0 or rect.height == 0:
        return surface

    cropped = pygame.Surface(rect.size, pygame.SRCALPHA)
    cropped.blit(surface, (0, 0), rect)
    return cropped


def fit_cover(surface, size):
    target_width, target_height = size
    source_width, source_height = surface.get_size()
    scale = max(target_width / source_width, target_height / source_height)
    scaled_size = (
        max(1, round(source_width * scale)),
        max(1, round(source_height * scale)),
    )
    scaled = pygame.transform.smoothscale(surface, scaled_size)

    crop_rect = pygame.Rect(
        max(0, (scaled_size[0] - target_width) // 2),
        max(0, (scaled_size[1] - target_height) // 2),
        target_width,
        target_height,
    )
    fitted = pygame.Surface(size, pygame.SRCALPHA)
    fitted.blit(scaled, (0, 0), crop_rect)
    return fitted


def load_image(filename):
    path = cfg.ASSET_DIR / filename
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error as error:
        raise SystemExit(f"Could not load image: {path}") from error

    image = remove_background(image)
    return crop_transparent_padding(image)


def load_raw_image(filename):
    path = cfg.ASSET_DIR / filename
    try:
        return pygame.image.load(path).convert_alpha()
    except pygame.error as error:
        raise SystemExit(f"Could not load image: {path}") from error


def split_toggle_image(surface):
    width, height = surface.get_size()
    top = pygame.Surface((width, height // 2), pygame.SRCALPHA)
    bottom = pygame.Surface((width, height - height // 2), pygame.SRCALPHA)
    top.blit(surface, (0, 0), pygame.Rect(0, 0, width, height // 2))
    bottom.blit(surface, (0, 0), pygame.Rect(0, height // 2, width, height - height // 2))
    return crop_transparent_padding(remove_background(top)), crop_transparent_padding(remove_background(bottom))


def make_pause_button():
    surface = pygame.Surface(cfg.PAUSE_BUTTON_SIZE, pygame.SRCALPHA)
    rect = surface.get_rect()
    pygame.draw.rect(surface, (32, 24, 16, 230), rect.inflate(-4, -4), border_radius=18)
    pygame.draw.rect(surface, (226, 190, 103), rect.inflate(-10, -10), border_radius=15)
    pygame.draw.rect(surface, (255, 220, 118), rect.inflate(-18, -18), border_radius=12)
    bar_width = 10
    bar_height = 34
    gap = 9
    start_x = rect.centerx - gap - bar_width
    for x in (start_x, start_x + bar_width + gap * 2):
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            pygame.Rect(x, rect.centery - bar_height // 2, bar_width, bar_height),
            border_radius=4,
        )
    return surface


def load_assets():
    bird_images = {
        name: fit_cover(load_image(filename), cfg.BIRD_SIZE)
        for name, filename in cfg.BIRD_IMAGES.items()
    }
    pillar_images = {
        name: load_image(filename)
        for name, filename in cfg.PILLAR_IMAGES.items()
    }

    ui_images = {}
    for name, filename in cfg.UI_IMAGES.items():
        if name == "background":
            ui_images[name] = fit_cover(load_raw_image(filename), (cfg.WIDTH, cfg.HEIGHT))
        elif name == "sound_toggle":
            on_image, off_image = split_toggle_image(load_raw_image(filename))
            ui_images["sound_on"] = on_image
            ui_images["sound_off"] = off_image
        elif name == "logo":
            ui_images[name] = fit_cover(load_image(filename), cfg.LOGO_SIZE)
        else:
            ui_images[name] = load_image(filename)
    ui_images["pause"] = make_pause_button()

    return {"bird": bird_images, "pillar": pillar_images, "ui": ui_images}


def get_scaled_image(image, size, flip_y=False):
    key = (id(image), size, flip_y)
    if key not in SCALED_IMAGE_CACHE:
        scaled = pygame.transform.smoothscale(image, size)
        if flip_y:
            scaled = pygame.transform.flip(scaled, False, True)
        SCALED_IMAGE_CACHE[key] = scaled
    return SCALED_IMAGE_CACHE[key]


def get_fitted_image(image, size, flip_y=False, vertical_anchor="center"):
    key = (id(image), size, flip_y, vertical_anchor)
    if key in SCALED_IMAGE_CACHE:
        return SCALED_IMAGE_CACHE[key]

    target_width, target_height = size
    source_width, source_height = image.get_size()
    scale = max(target_width / source_width, target_height / source_height)
    scaled_size = (
        max(1, round(source_width * scale)),
        max(1, round(source_height * scale)),
    )
    scaled = pygame.transform.smoothscale(image, scaled_size)

    if flip_y:
        scaled = pygame.transform.flip(scaled, False, True)

    crop_x = max(0, (scaled_size[0] - target_width) // 2)
    if vertical_anchor == "top":
        crop_y = 0
    elif vertical_anchor == "bottom":
        crop_y = max(0, scaled_size[1] - target_height)
    else:
        crop_y = max(0, (scaled_size[1] - target_height) // 2)

    fitted = pygame.Surface(size, pygame.SRCALPHA)
    fitted.blit(scaled, (0, 0), pygame.Rect(crop_x, crop_y, target_width, target_height))
    SCALED_IMAGE_CACHE[key] = fitted
    return fitted
