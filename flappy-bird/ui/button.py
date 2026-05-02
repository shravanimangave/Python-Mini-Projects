import pygame


class Button:
    def __init__(self, image, center, size=None, action=None, label=None):
        self.base_image = image
        if size is not None:
            self.base_image = pygame.transform.smoothscale(image, size)
        self.center = center
        self.action = action
        self.label = label
        self.hovered = False
        self.pressed = False
        self.rect = self.base_image.get_rect(center=center)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            clicked = self.pressed and self.rect.collidepoint(event.pos)
            self.pressed = False
            if clicked and self.action:
                self.action()
            return clicked

        return False

    def draw(self, surface):
        scale = 0.96 if self.pressed else 1.05 if self.hovered else 1.0
        width = max(1, round(self.base_image.get_width() * scale))
        height = max(1, round(self.base_image.get_height() * scale))
        image = pygame.transform.smoothscale(self.base_image, (width, height))
        if self.hovered and not self.pressed:
            image = image.copy()
            image.fill((24, 24, 24, 0), special_flags=pygame.BLEND_RGBA_ADD)
        rect = image.get_rect(center=self.center)
        surface.blit(image, rect)
        if self.label:
            font_size = max(22, round(rect.height * 0.28))
            font = pygame.font.Font(None, font_size)
            text = font.render(self.label, True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            surface.blit(text, text_rect)


class ToggleButton(Button):
    def __init__(self, on_image, off_image, center, size=None, enabled=True, action=None, label=None):
        self.on_image = on_image
        self.off_image = off_image
        self.enabled = enabled
        super().__init__(self.current_image, center, size, action, label)

    @property
    def current_image(self):
        return self.on_image if self.enabled else self.off_image

    def set_enabled(self, enabled):
        self.enabled = enabled
        size = self.base_image.get_size()
        self.base_image = pygame.transform.smoothscale(self.current_image, size)
        self.rect = self.base_image.get_rect(center=self.center)

    def handle_event(self, event):
        clicked = super().handle_event(event)
        if clicked:
            self.set_enabled(not self.enabled)
        return clicked
