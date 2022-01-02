import pygame
from pygame.locals import *
from components.events import events
from components.button import Button
from components.error import Error
from networking.client import client

class HostGameMenu():
    def __init__(self, size) -> None:
        self.size = size
        self.error = None
        self.init_bg()
        self.init_buttons()
        self.init_inputs()
        self.init_events()

    def init_bg(self):
        font = pygame.font.Font("./assets/fonts/RobotoMono-Regular.ttf", 32)
        text = font.render("Host Game", 1, (0,0,0))

        self.title = pygame.Surface((text.get_width() + 40, text.get_height() + 10), pygame.SRCALPHA)
        self.title.fill((255,255,255,100))
        self.title.blit(text, ((self.title.get_width() - text.get_width()) // 2, (self.title.get_height() - text.get_height())// 2))
        self.title_pos = ((self.size[0] - self.title.get_width()) // 2, 50)

        self.background = pygame.Surface(self.size, pygame.SRCALPHA)
        self.background.fill((150,150,150))

    def init_buttons(self):
        button_size = (200,40)
        button = pygame.Surface(button_size, pygame.SRCALPHA)
        button_color = (0,0,150,180)
        pygame.draw.rect(button, button_color, (0, 0, button_size[0], button_size[1]), border_radius=50)

        self.buttons = [
            Button(button, ((self.size[0] - button_size[0]) // 2, 390), "Create", self.create),
            Button(button, ((self.size[0] - button_size[0]) // 2, 450), "Back", self.back)
        ]

    def init_inputs(self):
        self.font = pygame.font.Font("./assets/fonts/RobotoMono-Regular.ttf", 20)

        self.input = pygame.Surface((200, 30))
        self.input.fill((255,255,255))
        pygame.draw.rect(self.input, (0,0,0), self.input.get_rect(), 3)

        self.room_input_rect = self.input.get_rect(midtop=(self.size[0] // 2, 220))
        self.username_input_rect = self.input.get_rect(midtop=(self.size[0] // 2, 150))

        self.room_input_active = False
        self.room_name = ""
        self.username_active = False

        username = self.font.render("Username", 1, (0,0,0))
        self.background.blit(username, (self.username_input_rect.left, self.username_input_rect.top - 25))
        self.background.blit(self.input, self.username_input_rect)

        room = self.font.render("Room name", 1, (0,0,0))
        self.background.blit(room, (self.room_input_rect.left, self.room_input_rect.top - 25))
        self.background.blit(self.input, self.room_input_rect)

    def init_events(self):
        events.sub("invalid room name", self.invalid_room_name)
        events.sub("remove host error", self.remove_error)

    def draw(self, surface):
        surface.blit(self.background, (0,0))
        surface.blit(self.title, self.title_pos)
        for button in self.buttons:
            button.draw(surface)
        if self.error:
            self.error.draw(surface)

        username = self.font.render(client.username, 1, (0,0,0))
        rect = username.get_rect(center=self.username_input_rect.center)
        surface.blit(username, rect)
        if self.username_active:
            pygame.draw.line(surface, (0,0,0), rect.topright, rect.bottomright)

        room_name = self.font.render(self.room_name, 1, (0,0,0))
        rect = room_name.get_rect(center=self.room_input_rect.center)
        surface.blit(room_name, rect)
        if self.room_input_active:
            pygame.draw.line(surface, (0,0,0), rect.topright, rect.bottomright)

    def update(self):
        self.event_handling()
        for button in self.buttons:
            button.update()
        if self.error:
            self.error.update()

    def create(self):
        if not client.username:
            self.set_error("Username is to short")
            return
        if not self.room_name:
            self.set_error("Room name is to short")
            return
        client.send("host game", [client.id, self.room_name, client.username])
        client.receive()

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
                    if self.username_input_rect.collidepoint(mouse_pos):
                        self.username_active = True
                    else:
                        self.username_active = False

                    if self.room_input_rect.collidepoint(mouse_pos):
                        self.room_input_active = True
                    else:
                        self.room_input_active = False

            elif event.type == KEYUP:
                if self.username_active or self.room_input_active:
                    if event.key == K_RETURN or event.key == K_ESCAPE:
                        self.username_active = False
                        self.room_input_active = False
                    elif event.key == K_BACKSPACE:
                        if self.username_active:
                            client.username = client.username[:-1]
                        elif self.room_input_active:
                            self.room_name = self.room_name[:-1]
                    else:
                        if self.username_active:
                            client.username += event.unicode
                        elif self.room_input_active:
                            self.room_name += event.unicode

    def set_error(self, text):
        self.error = Error(text, (self.size[0] // 2, 180), "remove host error")

    def remove_error(self):
        self.error = None

    def invalid_room_name(self):
        self.set_error("Room name already in use")
    