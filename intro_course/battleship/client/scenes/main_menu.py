import pygame
from pygame.locals import *
from components.events import events
from components.button import Button

class MainMenu():
    def __init__(self, size) -> None:
        self.size = size

        font = pygame.font.Font("./assets/fonts/RobotoMono-Regular.ttf", 32)
        text = font.render("Main Menu", 1, (0,0,0))

        self.title = pygame.Surface((text.get_width() + 40, text.get_height() + 10), pygame.SRCALPHA)
        self.title.fill((255,255,255,100))
        self.title.blit(text, ((self.title.get_width() - text.get_width()) // 2, (self.title.get_height() - text.get_height())// 2))
        self.title_pos = ((self.size[0] - self.title.get_width()) // 2, 50)

        self.background = pygame.Surface(self.size)
        self.background.fill((150,150,150))

        button_size = (200,40)
        button = pygame.Surface(button_size, pygame.SRCALPHA)
        button_color = (0,0,150,180)
        pygame.draw.rect(button, button_color, (0, 0, button_size[0], button_size[1]), border_radius=50)

        self.buttons = [
            Button(button, ((self.size[0] - button_size[0]) // 2, 330), "Host Game", self.host_game),
            Button(button, ((self.size[0] - button_size[0]) // 2, 390), "Join Game", self.join_game),
            Button(button, ((self.size[0] - button_size[0]) // 2, 450), "Quit Game", self.exit)
        ]

    def draw(self, surface):
        surface.blit(self.background, (0,0))
        surface.blit(self.title, self.title_pos)
        for button in self.buttons:
            button.draw(surface)

    def update(self):
        self.event_handling()
        for button in self.buttons:
            button.update()

    def join_game(self):
        events.post("switch scenes", "join game")

    def host_game(self):
        events.post("switch scenes", "host game")

    def exit(self):
        events.post("close app")

    def event_handling(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                events.post("close app")

            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for button in self.buttons:
                        if button.rect.collidepoint(mouse_pos):
                            mask_pos = (mouse_pos[0] - button.rect.x, mouse_pos[1] - button.rect.y)
                            if button.mask.get_at(mask_pos):
                                button.click()
                            break