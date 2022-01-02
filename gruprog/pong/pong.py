import pygame as py
from scenes.main_menu import Main_Menu
from components.events import events

class Window:
    def __init__(self):
        self.size = (784, 480)

        py.font.init()
        self.surface = py.display.set_mode(self.size)
        py.display.set_caption("Bloons clone")

        self.scenes = {
            "main menu": Main_Menu(self.size),
        }
        self.active_scene = self.scenes["main menu"]
        
        events.sub("close app", self.close)
        events.sub("switch scenes", self.switch_scenes)
        events.sub("start game", self.start_game)

    def start(self):
        self.running = True
        clock = py.time.Clock()
        while self.running:
            self.update()
            self.draw(self.surface)
            clock.tick(60)
        py.quit() 

    def draw(self, surface):
        self.active_scene.draw(surface)
        py.display.update()

    def update(self, ):
        self.active_scene.update()

    def close(self):
        self.running = False

    def switch_scenes(self, scene):
        self.active_scene = self.scenes[scene]
    
    def start_game(self):
        # self.scenes['game'] = Game(self.size, mapname)
        # self.active_scene = self.scenes['game']
        pass


if __name__ == "__main__":
    win = Window()
    win.start()