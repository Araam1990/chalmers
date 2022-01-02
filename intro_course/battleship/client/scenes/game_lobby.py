import pygame
from pygame.locals import *
from components.events import events
from networking.client import client
from components.button import Button

class GameLobby:
    def __init__(self, size, room_name, host, players) -> None:
        self.size = size
        self.room_name = room_name
        self.host = host
        self.players = players
        self.font = pygame.font.Font("./assets/fonts/RobotoMono-Regular.ttf", 20)
        self.username_midtop = (self.size[0] // 2, 120)
        self.init_bg()
        self.init_buttons()
        self.init_events()

    def init_bg(self):
        font = pygame.font.Font("./assets/fonts/RobotoMono-Regular.ttf", 32)
        text = font.render(f"Game Lobby {self.room_name}", 1, (0,0,0))

        self.title = pygame.Surface((text.get_width() + 40, text.get_height() + 10), pygame.SRCALPHA)
        self.title.fill((255,255,255,100))
        self.title.blit(text, ((self.title.get_width() - text.get_width()) // 2, (self.title.get_height() - text.get_height())// 2))
        self.title_pos = ((self.size[0] - self.title.get_width()) // 2, 50)

        self.background = pygame.Surface(self.size)
        self.background.fill((150,150,150))

    def init_buttons(self):
        self.button_size = (200,40)
        self.button = pygame.Surface(self.button_size, pygame.SRCALPHA)
        button_color = (0,0,150,180)
        pygame.draw.rect(self.button, button_color, (0, 0, self.button_size[0], self.button_size[1]), border_radius=50)

        self.buttons = []
        self.buttons.append(Button(self.button, ((self.size[0] - self.button_size[0]) // 2, 450), "Leave Room", self.leave))
        if self.host:
            self.is_host()
            
    def init_events(self):
        events.sub("player joined", self.add_player)
        events.sub("opponent left", self.opponent_left)
        events.sub("is host", self.is_host)

    def draw(self, surface):
        surface.blit(self.background, (0,0))
        surface.blit(self.title, self.title_pos)
        for i in range(len(self.players)):
            username = self.font.render(self.players[i], 1, (0,0,0))
            surface.blit(username, (self.username_midtop[0] - username.get_width() // 2,self.username_midtop[1] + i * 20))
        for button in self.buttons:
            button.draw(surface)

    def update(self):
        self.event_handling()
        for button in self.buttons:
            button.update()
        client.sender.send("dud", [client.id])
        client.receive()

    def start_game(self):
        if len(self.players) == 2:
            client.send("start game", [client.id])
            events.post("start game")

    def leave(self):
        client.send("leave room", [client.id])
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

    def add_player(self, username):
        self.players.append(username)

    def opponent_left(self):
        if self.players[0] == client.username:
            self.players.pop(1)
        elif self.players[1] == client.username:
            self.players.pop(0)
    
    def is_host(self):
        self.buttons.append(Button(self.button, ((self.size[0] - self.button_size[0]) // 2, 390), "Start Game", self.start_game))
