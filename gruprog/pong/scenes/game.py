import pygame
import json
from pygame.locals import *
from components.events import events
from game_entities.bloons import Bloon
from game_entities.towers.factory import tower_factory
from game_entities.shop import GameShop
from game_entities.overlay import Overlay

class Game():
    def __init__(self, size, mapname, save_file=None):
        self.size = size

        self.towers = []
        self.bloons = []
        self.moabs = []
        self.lives = 150
        self.money = 650
        self.two_times_speed = False
        self.wave = 0
        self.paused = True
        self.previewing_tower = None
        self.selected_tower = None
        self.bg_size = ((size[1] * 4) // 3, size[1])
        self.shop = GameShop((self.bg_size[0], 0), (self.size[0] - self.bg_size[0], self.size[1]))
        self.overlay = Overlay()
        self.game_over = False

        self.bg = pygame.transform.smoothscale(pygame.image.load(f"./maps/{mapname}/{mapname}.png"), self.bg_size)

        water_surface = pygame.transform.smoothscale(pygame.image.load(f"./maps/{mapname}/{mapname}_water.png"), self.bg_size)
        self.water_mask = pygame.mask.from_surface(water_surface)

        self.inverted_water_mask = self.water_mask.copy()
        self.inverted_water_mask.invert()

        unplaceable_surface = pygame.transform.smoothscale(pygame.image.load(f"./maps/{mapname}/{mapname}_unplaceable.png"), self.bg_size)
        self.unplaceable_mask = pygame.mask.from_surface(unplaceable_surface)

        path_file = open(f"./maps/{mapname}/{mapname}_path.json")
        self.path = json.load(path_file)
        path_file.close()

        self.total_dist = 0
        for i in range(1, len(self.path)):
            dist = (self.path[i][0] - self.path[i-1][0]) + (self.path[i][1] - self.path[i-1][1])
            if dist < 0:
                dist *= -1
            self.total_dist += dist

        for i in range(len(self.path)):
            self.path[i] = pygame.Vector2(self.path[i])

        events.sub("bloon made it through", self.bloon_went_through)
        events.sub("bloon dead", self.dead_bloon)
        events.sub("bloon popped", self.popped_bloon)
        events.sub("spawn bloon", self.spawn_bloon)
        events.sub("preview tower", self.preview_tower)
        events.sub("buy tower", self.buy_tower)
        events.sub("upgrade tower", self.upgrade_tower)
        events.sub("sell tower", self.sell_tower)

        if save_file:
            self.load_save(save_file)

    def draw(self, surface):
        surface.blit(self.bg, (0,0))

        if self.selected_tower:
            self.selected_tower.draw_range(surface)

        for bloon in self.bloons:
            bloon.draw(surface)

        for tower in self.towers:
            tower.draw(surface)

        if self.previewing_tower:
            self.previewing_tower.draw_range(surface)
            self.previewing_tower.draw(surface)

        for moab in self.moabs:
            moab.draw(surface)

        self.shop.draw(surface, self.money)
        if self.selected_tower:
            self.selected_tower.draw_menu(surface, self.money)
        self.overlay.draw_wave(surface, self.wave)
        self.overlay.draw_lives(surface, self.lives)
        self.overlay.draw_money(surface, self.money)

    def update(self):
        self.event_handling()
        for bloon in self.bloons:
            bloon.update()
        for moab in self.moabs:
            moab.update()
        if not self.game_over:
            for tower in self.towers:
                tower.update(self.bloons)
            if self.two_times_speed:
                for bloon in self.bloons:
                    bloon.update()
                for moab in self.moabs:
                    moab.update()
                for tower in self.towers:
                    tower.update(self.bloons)

    def event_handling(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.previewing_tower:
            self.previewing_tower.move(mouse_pos)
            if self.valid_placement(self.previewing_tower):
                self.previewing_tower.range_color = (0, 0, 0, 100)
            else:
                self.previewing_tower.range_color = (255, 0, 0, 100)

        for event in pygame.event.get():
            if event.type == QUIT:
                events.post("close app")

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if self.selected_tower:
                        if self.selected_tower.upgrade_menu.rect.collidepoint(mouse_pos):
                            self.selected_tower.upgrade_menu.click(mouse_pos)
                        else:
                            self.selected_tower.selected = False
                            self.selected_tower = None
                    if self.previewing_tower:
                        if self.valid_placement(self.previewing_tower):
                            events.post("buy tower", self.previewing_tower)
                            self.previewing_tower = None

                    elif self.shop.rect.collidepoint(mouse_pos):
                        self.shop.click(mouse_pos)

                    for tower in self.towers:
                        if tower.clicked(mouse_pos):
                            tower.selected = True
                            self.selected_tower = tower
                
                elif event.button == 3:
                    if self.previewing_tower:
                        self.previewing_tower = None

            elif event.type == KEYDOWN:
                if event.key == K_z:
                    self.spawn_bloon("red")
                elif event.key == K_x:
                    self.spawn_bloon("blue")
                elif event.key == K_c:
                    self.spawn_bloon("green")
                elif event.key == K_v:
                    self.spawn_bloon("yellow")
                elif event.key == K_f:
                    self.toggle_speed()
                elif event.key == K_ESCAPE:
                    if self.previewing_tower:
                        self.previewing_tower = None
    
    def valid_placement(self, tower):
        for tower2 in self.towers:
            if tower2.collide(tower):
                return False
        
        map_offset = (tower.pos[0] - tower.footprint, tower.pos[1] - tower.footprint)

        if tower.terrain == "land" and self.water_mask.overlap(tower.footprint_mask, map_offset):
            return False

        if tower.terrain == "water" and self.inverted_water_mask.overlap(tower.footprint_mask, map_offset):
            return False

        if self.unplaceable_mask.overlap(tower.footprint_mask, map_offset):
            return False

        if tower.pos[0] + tower.footprint > self.bg_size[0]:
            return False

        if tower.pos[1] + tower.footprint > self.bg_size[1]:
            return False

        return True

    def spawn_bloon(self, type):
        self.bloons.append(Bloon(type, self.path, self.total_dist))

    def bloon_went_through(self, bloon):
        if not self.game_over:
            self.lives -= bloon.hp
            if self.lives <= 0:
                self.lives = 0
                self.game_over = True

        high = len(self.bloons) - 1
        low = 0
        i = 0
        while self.bloons[i].id != bloon.id:
            i = (high + low) // 2
            if self.bloons[i].id < bloon.id:
                low = i + 1
            else:
                high = i - 1
        del self.bloons[i]

    def popped_bloon(self):
        self.money += 1

    def dead_bloon(self, bloon_id):
        high = len(self.bloons) - 1
        low = 0
        i = 0
        while self.bloons[i].id != bloon_id:
            i = (high + low) // 2
            if self.bloons[i].id < bloon_id:
                low = i + 1
            else:
                high = i - 1
        del self.bloons[i]
        self.money += 1

    def toggle_speed(self):
        self.two_times_speed = not self.two_times_speed
    
    def preview_tower(self, tower_name):
        tower = tower_factory(tower_name, pygame.mouse.get_pos())
        if tower.price <= self.money:
            self.previewing_tower = tower
    
    def buy_tower(self, tower):
        self.towers.append(tower)
        self.money -= tower.price

    def upgrade_tower(self, tower_id, upgrade):
        if upgrade.price < self.money:
            events.post(f"tower-{tower_id} upgrade", upgrade)
            self.money -= upgrade.price

    def sell_tower(self, tower):
        self.towers.append(tower)
        self.money -= tower.price

    def load_save(self, save):
        self.towers = save["towers"]
        self.lives = save["lives"]
        self.money = save["money"]
        self.wave = save["wave"]