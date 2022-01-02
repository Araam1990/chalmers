import pygame
from pygame import Vector2 as v2
from pygame.locals import *
from components.events import events


class Player:
    def __init__(self, players = None):
        self.username = ""
        self.id = None
        self.players = players
    
    def draw(self, surface):
        pass

    def update(self, display_rect):
        pass