import pygame, json
from pygame.locals import *
from components.events import events
from components.player import Player
from components.game_overlay import GameOverlay

from networking.client import Client

class Game():
    def __init__(self, size) -> None:
        self.size = size
        self.players = []


    def draw(self, surface):
        surface.fill((0,255,0))

    def update(self):
        self.event_handling()

    def event_handling(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                events.post("close app")

            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
