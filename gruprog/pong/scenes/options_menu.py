import pygame
from pygame.locals import *
from components.buttons.menu_button import MenuButton
from components.events import events

class Options_Menu():
    def __init__(self, size):
        self.size = size

        self.bg = pygame.image.load("./images/menu_bg.png")
        self.bg = pygame.transform.smoothscale(self.bg, self.size)
        font = pygame.font.Font("Roboto_Mono/static/RobotoMono-Regular.ttf", 32)
        text = font.render("Options", 1, (0,0,0))

        title_surface = pygame.Surface((text.get_width() + 40, text.get_height() + 10), pygame.SRCALPHA)
        title_surface.fill((255,255,255,100))
        title_surface.blit(text, ((title_surface.get_width() - text.get_width()) // 2, (title_surface.get_height() - text.get_height())// 2))

        self.bg.blit(title_surface, ((self.bg.get_width() - title_surface.get_width()) // 2, 50))

        button_size = (160,50)
        self.buttons = [
            MenuButton("Back", ((size[0] - button_size[0]) // 2,400), button_size, self.back)
        ]

    def draw(self, surface):
        surface.blit(self.bg, (0,0))
        for button in self.buttons:
            button.draw(surface)

    def update(self):
        self.event_handling()
        for button in self.buttons:
            button.update()

    def back(self):
        events.post("switch scenes", "main menu")

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
                    
