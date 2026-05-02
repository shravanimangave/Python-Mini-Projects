import pygame

import settings as cfg


def draw_text(surface, font, text, color, center):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    surface.blit(rendered, rect)


def draw_panel(surface, rect, fill=(22, 34, 30, 210), border=(236, 210, 132)):
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(panel, fill, panel.get_rect(), border_radius=24)
    pygame.draw.rect(panel, border, panel.get_rect(), width=3, border_radius=24)
    surface.blit(panel, rect)


def draw_score_panel(surface, font, score, best_score):
    rect = pygame.Rect(18, 18, 160, 74)
    draw_panel(surface, rect, fill=(18, 28, 26, 170))
    draw_text(surface, font, f"Score {score}", (255, 255, 255), rect.center)
    draw_text(surface, font, f"Best {best_score}", (230, 220, 170), (rect.centerx, rect.centery + 24))


def draw_game_over_panel(surface, fonts, score, best_score):
    rect = pygame.Rect(42, 180, cfg.WIDTH - 84, 250)
    draw_panel(surface, rect)
    draw_text(surface, fonts["large"], "GAME OVER", (255, 235, 185), (cfg.WIDTH // 2, rect.top + 58))
    draw_text(surface, fonts["medium"], f"Score: {score}", (255, 255, 255), (cfg.WIDTH // 2, rect.top + 128))
    draw_text(surface, fonts["medium"], f"Best: {best_score}", (255, 220, 120), (cfg.WIDTH // 2, rect.top + 178))


def draw_pause_overlay(surface, fonts):
    overlay = pygame.Surface((cfg.WIDTH, cfg.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 135))
    surface.blit(overlay, (0, 0))
    draw_text(surface, fonts["large"], "PAUSED", (255, 255, 255), (cfg.WIDTH // 2, 210))
