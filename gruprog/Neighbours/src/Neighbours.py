from hashlib import new
from typing import List
from enum import Enum, auto
from random import *
from time import perf_counter
from copy import deepcopy

import pygame as pg


#  Program to simulate segregation.
#  See : http:#nifty.stanford.edu/2014/mccown-schelling-model-segregation/
#

# Enumeration type for the Actors
class Actor(Enum):
    BLUE = auto()
    RED = auto()
    NONE = auto()  # NONE used for empty locations


# Enumeration type for the state of an Actor
class State(Enum):
    UNSATISFIED = auto()
    SATISFIED = auto()
    NA = auto()  # Not applicable (NA), used for NONEs


World = List[List[Actor]]  # Type alias


SIZE = 300


def neighbours():
    pg.init()
    model = NeighboursModel(SIZE)
    _view = NeighboursView(model)
    model.run()


class NeighboursModel:

    # Tune these numbers to test different distributions or update speeds
    FRAME_RATE = 30            # Increase number to speed simulation up
    DIST = [0.25, 0.25, 0.50]  # % of RED, BLUE, and NONE
    THRESHOLD = 0.7            # % of surrounding neighbours that should be like me for satisfaction

    # ########### These following two methods are what you're supposed to implement  ###########
    # In this method you should generate a new world
    # using randomization according to the given arguments.
    def __create_world(self, size, dist) -> World:
        world, empty_positions = self.__create_empty_world(size)
        world, empty_positions = self.__add_red_actors(world, dist, empty_positions)
        world, empty_positions = self.__add_blue_actors(world, dist, empty_positions)
        return world

    @staticmethod
    def __create_empty_world(size):
        world = []
        positions = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(Actor.NONE)
                positions.append((i,j))
            world.append(row)
        return world, positions

    def __add_red_actors(self, world, dist, empty_positions):
        amount = int(len(world) * len(world[1]) * dist[0])
        return self.__add_actors(world, empty_positions, amount, Actor.RED)

    def __add_blue_actors(self, world, dist, empty_positions):
        amount = int(len(world) * len(world[1]) * dist[1])
        return self.__add_actors(world, empty_positions, amount, Actor.BLUE)

    @staticmethod
    def __add_actors(world, empty_positions, amount, color):
        for _ in range(amount):
            idx = randint(0, len(empty_positions) - 1)
            pos = empty_positions.pop(idx)
            world[pos[0]][pos[1]] = color
        return world, empty_positions

    # This is the method called by the timer to update the world
    # (i.e move unsatisfied) each "frame".
    def __update_world(self):
        unsatisfied, empty_positions = self.get_unsatisfied(self.world, self.THRESHOLD)
        world = self.set_unsatisfied_to_none(self.world, unsatisfied)
        self.world = self.move_unsatisfied(world, unsatisfied, empty_positions)

    @staticmethod
    def get_unsatisfied(world, th):
        unsatisfied = []
        empty_positions = []
        for row in range(len(world)):
            for col in range(len(world[0])):
                if world[row][col] != Actor.NONE:
                    if NeighboursModel.is_unsatisfied(world, row, col, th):
                        unsatisfied.append((world[row][col], (row,col)))
                        empty_positions.append((row,col))
                else:
                    empty_positions.append((row,col))
        return unsatisfied, empty_positions

    @staticmethod
    def is_unsatisfied(world, row, col, th):
        neighbours = NeighboursModel.get_neighbours(world, row, col)
        if len(neighbours) == 0:
            return False
        same_color = NeighboursModel.color_count(neighbours, world[row][col])
        return same_color / len(neighbours) < th

    @staticmethod
    def get_neighbours(world, row, col):
        offsets = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1 ),
            (1, -1),
            (1, 0),
            (1, 1)
        ]
        neighbours = []
        for offset in offsets:
            new_row, new_col = row + offset[0], col + offset[1]
            if is_valid_location(len(world), new_row, new_col) and world[new_row][new_col] != Actor.NONE:
                neighbours.append(world[new_row][new_col])
        return neighbours

    @staticmethod
    def color_count(neighbours, color):
        count = 0
        for neighbour in neighbours:
            if neighbour == color:
                count += 1
        return count

    @staticmethod
    def set_unsatisfied_to_none(world, unsatisfied):
        for _, pos in unsatisfied:
            world[pos[0]][pos[1]] = Actor.NONE
        return world

    @staticmethod
    def move_unsatisfied(world, unsatisfied, empty_positions):
        for i ,(color, _) in enumerate(unsatisfied):
            new_pos_idx = randint(i, len(empty_positions) - 1)
            new_pos = empty_positions[new_pos_idx]
            empty_positions[new_pos_idx] = empty_positions[i]
            world[new_pos[0]][new_pos[1]] = color
        return world

    # ########### the rest of this class is already defined, to handle the simulation clock  ###########
    def __init__(self, size):
        self.world: World = self.__create_world(size, self.DIST)
        self.observers = []  # for enabling discoupled updating of the view, ignore

    def run(self):
        clock = pg.time.Clock()
        running = True
        while running:
            running = self.__on_clock_tick(clock)
        # stop running
        print("Goodbye!")
        pg.quit()

    def __on_clock_tick(self, clock):
        clock.tick(self.FRAME_RATE)  # update no faster than FRAME_RATE times per second
        self.__update_and_notify()
        return self.__check_for_exit()

    # What to do each frame
    def __update_and_notify(self):
        self.__update_world()
        self.__notify_all()

    def __check_for_exit(self) -> bool:
        keep_going = True
        for event in pg.event.get():
            # Did the user click the window close button?
            if event.type == pg.QUIT:
                keep_going = False
            elif event.type == pg.KEYUP:
                if event.key == pg.K_PLUS:
                    self.FRAME_RATE += 1
                elif event.key == pg.K_MINUS and self.FRAME_RATE > 1:
                    self.FRAME_RATE -= 1
        return keep_going

    # Use an Observer pattern for views
    def add_observer(self, observer):
        self.observers.append(observer)

    def __notify_all(self):
        for observer in self.observers:
            observer.on_world_update()


# ---------------- Helper methods ---------------------

# Check if inside world
def is_valid_location(size: int, row: int, col: int):
    return 0 <= row < size and 0 <= col < size


# ------- Testing -------------------------------------

# Here you run your tests i.e. call your logic methods
# to see that they really work
def test():
    global SIZE
    # A small hard coded world for testing
    test_world = [
        [Actor.RED, Actor.RED, Actor.NONE],
        [Actor.RED, Actor.BLUE, Actor.NONE],
        [Actor.BLUE, Actor.NONE, Actor.BLUE]
    ]

    th = 0.5  # Simpler threshold used for testing

    valid_location_tests(test_world)
    neighbours_tests(test_world)
    is_unsatisfied_tests(test_world, th)
    get_unsatisfied_tests(deepcopy(test_world), th)
    move_tests(deepcopy(test_world), th)

    exit(0)

def valid_location_tests(world):
    size = len(world)
    print("Valid location tests:")
    print(is_valid_location(size, 0, 0))
    print(not is_valid_location(size, -1, 0))
    print(not is_valid_location(size, 0, 3))
    print(is_valid_location(size, 2, 2))
    print("-----")

def is_unsatisfied_tests(world, th):
    print("Is unsatisfied tests:")
    print(not NeighboursModel.is_unsatisfied(world, 0,0, th))
    print(NeighboursModel.is_unsatisfied(world, 1,1, th))
    print("-----")

def neighbours_tests(world):
    print("Get neighbours tests:")

    corner_pos = NeighboursModel.get_neighbours(world, 2,2)
    print(len(corner_pos) == 3)
    print(count(corner_pos, Actor.BLUE) == 1)

    middle_pos = NeighboursModel.get_neighbours(world, 1,1)
    print(len(middle_pos) == 8)
    print(count(middle_pos, Actor.BLUE) == 2)

    middle_right_pos = NeighboursModel.get_neighbours(world, 1,2)
    print(len(middle_right_pos) == 5)
    print(count(middle_right_pos, Actor.RED) == 1)

    print("-----")

def get_unsatisfied_tests(world, th):
    print("Get unsatisfied tests:")
    unsatisfied, empty_positions = NeighboursModel.get_unsatisfied(world, th)
    print(len(unsatisfied) == 5)
    print(len(empty_positions) == 8)
    print((0,0) not in empty_positions)
    print("-----")

def move_tests(world, th):
    print("Move tests:")
    world_before_move = deepcopy(world)
    unsatisfied, empty_positions = NeighboursModel.get_unsatisfied(world, th)
    world = NeighboursModel.move_unsatisfied(world, unsatisfied, empty_positions)
    print(not world_before_move == world)
    print("-----")

# Helper method for testing
def count(a_list, to_find):
    the_count = 0
    for a in a_list:
        if a == to_find:
            the_count += 1
    return the_count


# ###########  NOTHING to do below this row, it's pygame display stuff  ###########
# ... but by all means have a look at it, it's fun!
class NeighboursView:
    # static class variables
    WIDTH = 800   # Size for window
    HEIGHT = 800
    MARGIN = 10

    WHITE = (50, 50, 50)
    RED   = (245,   90,   0)
    BLUE  = (  9,   186, 190)

    # Instance methods

    def __init__(self, model: NeighboursModel):
        pg.init()  # initialize pygame, in case not already done
        self.dot_size = self.__calculate_dot_size(len(model.world))
        self.screen = pg.display.set_mode([self.WIDTH, self.HEIGHT])
        self.model = model
        self.model.add_observer(self)
        self.font = pg.font.SysFont(pg.font.get_fonts()[0], 20)
        self.__last_updates = [perf_counter()]

    def render_world(self):
        # # Render the state of the world to the screen
        self.__draw_background()
        self.__draw_all_actors()
        self.__draw_fps()
        self.__update_screen()

    # Needed for observer pattern
    # What do we do every time we're told the model had been updated?
    def on_world_update(self):
        self.render_world()

    # private helper methods
    def __calculate_dot_size(self, size):
        return max((self.WIDTH - 2 * self.MARGIN) / size, 2)

    @staticmethod
    def __update_screen():
        pg.display.flip()

    def __draw_background(self):
        self.screen.fill(NeighboursView.WHITE)

    def __draw_all_actors(self):
        for row in range(len(self.model.world)):
            for col in range(len(self.model.world[row])):
                self.__draw_actor_at(col, row)

    def __draw_actor_at(self, col, row):
        color = self.__get_color(self.model.world[row][col])
        xy = self.__calculate_coordinates(col, row)
        pg.draw.circle(self.screen, color, xy, self.dot_size / 2)

    def __draw_fps(self):
        new_update = perf_counter()
        self.__last_updates.append(new_update)
        index = None
        for i in range(len(self.__last_updates)):
            if new_update - self.__last_updates[::-1][i] >= 1:
                index = i
                break
        if index:
            self.__last_updates = self.__last_updates[-index:]
        fps = len(self.__last_updates)
        text = self.font.render(f"{fps}", 1, (0,0,0))
        self.screen.blit(text, (5, 5))

    # This method showcases how to nicely emulate 'switch'-statements in python
    @staticmethod
    def __get_color(actor):
        return {
            Actor.RED: NeighboursView.RED,
            Actor.BLUE: NeighboursView.BLUE
        }.get(actor, NeighboursView.WHITE)

    def __calculate_coordinates(self, col, row):
        x = self.__calculate_coordinate(col)
        y = self.__calculate_coordinate(row)
        return x, y

    def __calculate_coordinate(self, offset):
        x: float = self.dot_size * offset + self.MARGIN
        return x

if __name__ == "__main__":
    neighbours()
    # test()