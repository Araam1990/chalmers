import pygame
from pygame.locals import *
from components.events import events

class Main_Menu():
    def __init__(self, size):
        self.size = size

        self.bg = pygame.Surface(self.size)
        font = pygame.font.Font("Roboto_Mono/static/RobotoMono-Regular.ttf", 32)
        text = font.render("Main Menu", 1, (0,0,0))

        title_surface = pygame.Surface((text.get_width() + 40, text.get_height() + 10), pygame.SRCALPHA)
        title_surface.fill((255,255,255,100))
        title_surface.blit(text, ((title_surface.get_width() - text.get_width()) // 2, (title_surface.get_height() - text.get_height())// 2))

        self.bg.blit(title_surface, ((self.bg.get_width() - title_surface.get_width()) // 2, 40))

        button_size = (160,50)

        self.buttons = [
            MenuButton("New game" , ((size[0] - 160) // 2,220), button_size, self.new_game),
            MenuButton("Load game", ((size[0] - 160) // 2,280), button_size, self.load_game),
            MenuButton("Options"  , ((size[0] - 160) // 2,340), button_size, self.options),
            MenuButton("Exit"     , ((size[0] - 160) // 2,400), button_size, self.exit)
        ]

    def draw(self, surface):
        surface.blit(self.bg, (0,0))
        for button in self.buttons:
            button.draw(surface)

    def update(self):
        self.event_handling()
        for button in self.buttons:
            button.update()

    def new_game(self):
        events.post("switch scenes", "new game menu")

    def load_game(self):
        pass
        # events.post("switch scenes", "load game")

    def options(self):
        events.post("switch scenes", "options")

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
                    
