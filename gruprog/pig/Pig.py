import random

class Dice:
    def __init__(self):
        self.values = [1,2,3,4,5,6]

    def roll(self):
        index = random.randint(0,len(self.values) - 1)
        return self.values[index]

class Player:
    def __init__(self, points, name=''):
        self.name = name
        self.total_points = 0
        self.round_points = 0
        self.win_points = points
        self.dice = Dice()

    def roll(self):
        dice_value = self.dice.roll()
        if dice_value == 1:
            self.round_points = 0
            return True
        else:
            self.round_points = self.round_points + dice_value
            round_msg(dice_value, self)
            
    def win_check(self):
        if (self.total_points + self.round_points >= self.win_points):
                return True
    
    def save_points(self):
        self.total_points += self.round_points
        self.round_points = 0

class Game:
    def __init__(self):
        self.win_points = int(input("Enter the amount of points needed to win > "))
        self.players = self.set_players()
        self.cur_player = random.randint(0, len(self.players)-1)
        self.state = "playing"

    def set_players(self):
        players = []
        players_amount = int(input("Enter the number of players > "))
        for i in range(players_amount):
            name = input(f"Enter name for player {i + 1} > ")
            players.append(Player(self.win_points, name))
        return players

    def run(self):
        status_msg(self.players)

        self.game_loop()

        game_over_msg(self.player, self.state)
    
    def game_loop(self):
        while True:
            nextmove = get_player_choice(self.player)
            if nextmove == "n":
                self.player.save_points()
                self.next()
            if nextmove == "r":
                if self.player.roll():
                    print("Player got a 1 and lost it all")
                    self.next()
                if self.player.win_check():
                    break
            if nextmove == "q":
                self.state = "aborted"
                break

    def next(self):
        self.player.total_points = self.player.total_points + self.player.round_points
        self.player.round_points = 0
        self.cur_player = (self.cur_player+1)%(len(self.players))
        status_msg(self.players)

    @property
    def player(self):
        return self.players[self.cur_player]


# ---- Game logic methods --------------





# ---- IO Methods --------------
def welcome_msg(win_pts):
    print("Welcome to PIG!")
    print(f"First player to get {win_pts} points will win!")
    print("Commands are: r = roll , n = next, q = quit")


def status_msg(the_players):
    print("Points: ")
    for player in the_players:
        print(f"\t{player.name} = {player.total_points} ")


def round_msg(result, current_player):
    if result > 1:
        print(f"You got a {result}")
        print(f"Your running total is now {current_player.round_points}")
    else:
        print("You got a 1 and lost it all!")


def game_over_msg(player, state):
    if state == "aborted":
        print("Aborted")
    else:
        print(f"Game over! Winner is player {player.name} with {player.total_points + player.round_points} points")


def get_player_choice(player):
    return input(f"Player is {player.name} > ")


if __name__ == "__main__":
    game = Game()
    game.run()