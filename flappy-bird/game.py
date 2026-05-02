from enum import Enum, auto

import pygame

import settings as cfg
from entities.bird import Bird
from entities.pipe import PipePair
from ui.button import Button, ToggleButton
from ui.panels import draw_game_over_panel, draw_pause_overlay, draw_score_panel, draw_text
from utils.assets import get_fitted_image
from utils.collision import bird_hit_bounds, update_pipe_collisions_and_score
from utils.storage import load_best_score, save_best_score


class GameState(Enum):
    START_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class SkyDashGame:
    def __init__(self, assets, sounds, fonts):
        self.assets = assets
        self.sounds = sounds
        self.fonts = fonts
        self.state = GameState.START_MENU
        self.score = 0
        self.best_score = load_best_score()
        self.sound_enabled = True
        self.music_enabled = True
        self.show_menu_settings = False
        self.request_quit = False
        self.reset_run()
        self.create_buttons()

    def reset_run(self):
        self.bird = Bird(self.assets["bird"])
        self.pipes = []
        self.score = 0
        self.last_pipe_time = pygame.time.get_ticks()
        self.waiting_to_start = True

    def create_buttons(self):
        ui = self.assets["ui"]
        self.menu_buttons = [
            Button(ui["play"], (cfg.WIDTH // 2, 365), cfg.BUTTON_SIZE, self.start_game),
            Button(ui["settings"], (cfg.WIDTH // 2, 495), cfg.BUTTON_SIZE, self.toggle_menu_settings),
            Button(ui["exit"], (cfg.WIDTH // 2, 625), cfg.SQUARE_BUTTON_SIZE, self.quit_game),
        ]
        self.game_buttons = [
            Button(ui["pause"], (cfg.WIDTH - 48, 48), cfg.PAUSE_BUTTON_SIZE, self.pause_game),
        ]
        self.pause_buttons = [
            Button(ui["play"], (cfg.WIDTH // 2, 300), cfg.BUTTON_SIZE, self.resume_game),
            Button(ui["home"], (cfg.WIDTH // 2, 420), cfg.BUTTON_SIZE, self.go_home),
            Button(ui["exit"], (cfg.WIDTH // 2, 530), cfg.SQUARE_BUTTON_SIZE, self.quit_game),
        ]
        self.game_over_buttons = [
            Button(ui["retry"], (cfg.WIDTH // 2, 520), cfg.BUTTON_SIZE, self.start_game),
            Button(ui["home"], (cfg.WIDTH // 2, 650), cfg.BUTTON_SIZE, self.go_home),
        ]
        self.sound_toggle = ToggleButton(
            ui["sound_on"],
            ui["sound_off"],
            (cfg.WIDTH // 2, 610),
            cfg.TOGGLE_BUTTON_SIZE,
            self.sound_enabled,
            self.toggle_sound,
        )
        self.music_toggle = ToggleButton(
            ui["sound_on"],
            ui["sound_off"],
            (cfg.WIDTH // 2, 700),
            cfg.TOGGLE_BUTTON_SIZE,
            self.music_enabled,
            self.toggle_music,
        )

    def play_sound(self, name):
        if self.sound_enabled:
            self.sounds[name].play()

    def start_game(self):
        self.reset_run()
        self.show_menu_settings = False
        self.state = GameState.PLAYING

    def pause_game(self):
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED

    def resume_game(self):
        if self.state == GameState.PAUSED:
            self.last_pipe_time = pygame.time.get_ticks()
            self.state = GameState.PLAYING

    def go_home(self):
        self.reset_run()
        self.show_menu_settings = False
        self.state = GameState.START_MENU

    def quit_game(self):
        self.request_quit = True

    def toggle_menu_settings(self):
        self.show_menu_settings = not self.show_menu_settings

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled

    def toggle_music(self):
        self.music_enabled = not self.music_enabled

    def flap(self):
        if self.state == GameState.PLAYING and not self.bird.dead:
            if self.waiting_to_start:
                self.waiting_to_start = False
                self.last_pipe_time = pygame.time.get_ticks()
            self.bird.flap()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                if self.state == GameState.PLAYING:
                    self.pause_game()
                elif self.state == GameState.PAUSED:
                    self.resume_game()
            elif event.key == pygame.K_SPACE or (event.key == pygame.K_UP and not self.waiting_to_start):
                self.flap()

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.state == GameState.PLAYING
            and not self.waiting_to_start
            and not any(button.rect.collidepoint(event.pos) for button in self.game_buttons)
        ):
            self.flap()

        if self.state == GameState.START_MENU:
            self.handle_start_menu_event(event)
        elif self.state == GameState.PLAYING:
            self.handle_playing_event(event)
        elif self.state == GameState.PAUSED:
            self.handle_paused_event(event)
        elif self.state == GameState.GAME_OVER:
            self.handle_game_over_event(event)

    def handle_start_menu_event(self, event):
        if self.show_menu_settings:
            self.sound_toggle.handle_event(event)
            self.music_toggle.handle_event(event)
            self.menu_buttons[1].handle_event(event)
            return

        for button in self.menu_buttons:
            button.handle_event(event)

    def handle_playing_event(self, event):
        for button in self.game_buttons:
            button.handle_event(event)

    def handle_paused_event(self, event):
        self.sound_toggle.handle_event(event)
        self.music_toggle.handle_event(event)
        for button in self.pause_buttons:
            button.handle_event(event)

    def handle_game_over_event(self, event):
        for button in self.game_over_buttons:
            button.handle_event(event)

    def update(self):
        if self.state == GameState.PLAYING:
            self.update_playing()
        elif self.state == GameState.GAME_OVER:
            self.update_dead_bird()

    def update_playing(self):
        if self.waiting_to_start:
            return

        now = pygame.time.get_ticks()
        self.bird.update()

        if now - self.last_pipe_time >= cfg.PIPE_INTERVAL_MS:
            self.pipes.append(
                PipePair(
                    cfg.WIDTH + cfg.PIPE_WIDTH,
                    self.assets["pillar"],
                    get_fitted_image,
                )
            )
            self.last_pipe_time = now

        for pipe in self.pipes:
            pipe.update()

        score_gain, hit_pipe = update_pipe_collisions_and_score(self.bird, self.pipes)
        if score_gain:
            self.score += score_gain
            self.play_sound("score")

        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]

        if hit_pipe or bird_hit_bounds(self.bird):
            self.end_run()

    def update_dead_bird(self):
        if self.bird.rect.bottom < cfg.PLAYABLE_HEIGHT:
            self.bird.update(animate=False)

    def end_run(self):
        self.bird.kill()
        if self.score > self.best_score:
            self.best_score = self.score
            save_best_score(self.best_score)
        self.play_sound("crash")
        self.state = GameState.GAME_OVER

    def draw(self, surface):
        if self.state == GameState.START_MENU:
            self.draw_start_menu(surface)
        elif self.state == GameState.PLAYING:
            self.draw_playing(surface)
        elif self.state == GameState.PAUSED:
            self.draw_world(surface)
            draw_score_panel(surface, self.fonts["small"], self.score, self.best_score)
            self.draw_paused(surface)
        elif self.state == GameState.GAME_OVER:
            self.draw_world(surface)
            self.draw_game_over(surface)

    def draw_background(self, surface):
        surface.blit(self.assets["ui"]["background"], (0, 0))

    def draw_world(self, surface):
        self.draw_background(surface)
        for pipe in self.pipes:
            pipe.draw(surface)
        self.bird.draw(surface)

    def draw_start_menu(self, surface):
        self.draw_background(surface)
        logo = self.assets["ui"]["logo"]
        surface.blit(logo, logo.get_rect(center=(cfg.WIDTH // 2, 160)))
        for button in self.menu_buttons:
            button.draw(surface)
        if self.show_menu_settings:
            settings_rect = pygame.Rect(36, 555, cfg.WIDTH - 72, 185)
            overlay = pygame.Surface(settings_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(overlay, (9, 20, 18, 190), overlay.get_rect(), border_radius=22)
            surface.blit(overlay, settings_rect)
            draw_text(surface, self.fonts["small"], "Sound", (255, 255, 255), (cfg.WIDTH // 2 - 118, 610))
            draw_text(surface, self.fonts["small"], "Music", (255, 255, 255), (cfg.WIDTH // 2 - 118, 700))
            self.sound_toggle.draw(surface)
            self.music_toggle.draw(surface)

    def draw_playing(self, surface):
        self.draw_world(surface)
        draw_score_panel(surface, self.fonts["small"], self.score, self.best_score)
        if self.waiting_to_start:
            draw_text(surface, self.fonts["medium"], "Press Space to Start", (255, 255, 255), (cfg.WIDTH // 2, 300))
        for button in self.game_buttons:
            button.draw(surface)

    def draw_paused(self, surface):
        draw_pause_overlay(surface, self.fonts)
        draw_text(surface, self.fonts["small"], "Sound", (255, 255, 255), (cfg.WIDTH // 2 - 118, 610))
        draw_text(surface, self.fonts["small"], "Music", (255, 255, 255), (cfg.WIDTH // 2 - 118, 700))
        for button in self.pause_buttons:
            button.draw(surface)
        self.sound_toggle.draw(surface)
        self.music_toggle.draw(surface)

    def draw_game_over(self, surface):
        draw_game_over_panel(surface, self.fonts, self.score, self.best_score)
        for button in self.game_over_buttons:
            button.draw(surface)


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
