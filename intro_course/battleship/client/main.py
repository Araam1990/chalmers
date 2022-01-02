import pygame
from scenes.main_menu import MainMenu
from scenes.host_game import HostGameMenu
from scenes.join_game import JoinGameMenu
from scenes.game_lobby import GameLobby
from scenes.game import Game
from components.events import events

class Window:
    def __init__(self):
        self.size = (400, 600)

        pygame.font.init()
        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Battleship")

        self.scenes = {
            "main menu": MainMenu(self.size),
            "host game": HostGameMenu(self.size),
            "join game": JoinGameMenu(self.size),
        }
        self.active_scene = self.scenes["main menu"]

        self.background = pygame.Surface(self.size)
        self.background.fill((0,0,0))
        
        events.sub("close app", self.close)
        events.sub("switch scenes", self.switch_scenes)
        events.sub("join game", self.join_game)
        events.sub("game lobby", self.game_lobby)
        events.sub("start game", self.start_game)

    def start(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            self.update()
            self.draw(self.surface)
            clock.tick(60)
        pygame.quit() 

    def draw(self, surface):
        self.active_scene.draw(surface)
        pygame.display.update()

    def update(self):
        self.active_scene.update()

    def close(self):
        self.running = False

    def switch_scenes(self, scene):
        self.active_scene = self.scenes[scene]
    
    def join_game(self):
        self.scenes['game'] = Game(self.size)
        self.active_scene = self.scenes['game']
    
    def game_lobby(self, *args):
        self.active_scene = GameLobby(self.size, *args)

    def start_game(self, *args):
        self.active_scene = Game(self.size, *args)



if __name__ == "__main__":
    win = Window()
    win.start()