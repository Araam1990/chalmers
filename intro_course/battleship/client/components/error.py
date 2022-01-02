import pygame
from components.events import events

class Error:
    def __init__(self, text, pos, callbackevent=""):
        self.font = pygame.font.Font("./assets/fonts/RobotoMono-Regular.ttf", 24)
        self.callbackevent = callbackevent
        text = self.font.render(text, 0, (255,255,255))
        self.image = pygame.Surface((text.get_width() + 20, text.get_height() + 20), pygame.SRCALPHA)
        self.image.fill((255,0,0, 170))
        self.image.blit(text, text.get_rect(center=self.image.get_rect().center))
        self.rect = self.image.get_rect(midtop=pos)
        self.lifetime = 90

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.lifetime -= 1
        if self.lifetime == 0:
            events.post(self.callbackevent)