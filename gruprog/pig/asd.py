# /*
#  * The Pig game
#  * See http://en.wikipedia.org/wiki/Pig_%28dice_game%29
#  *
#  */

import random

def run():
    win_points = 5  # Points to win (decrease if testing)
    players, cur_player, cur_player_index = init_players()
    welcome_msg(win_points)
    status_msg(players)
    aborted, cur_player = game_loop(win_points, players, cur_player_index, cur_player)
    game_over_msg(cur_player, aborted)

def game_loop(win_points, players, cur_player_index, cur_player):
    while True:
        nextmove = get_player_choice(cur_player)
        if nextmove == "n":
            cur_player_index, cur_player, = next(cur_player_index, cur_player, players)
            status_msg(players)
        elif nextmove == "r":
            cur_player_index, cur_player, result = roll(cur_player_index, cur_player, players, 0)
            round_msg(result, cur_player)
            status_msg(players)
            if win_check(cur_player, win_points):
                cur_player.save_points()
                return False, cur_player
        elif nextmove == "q":
            return True, cur_player
        else:
            input_error(nextmove)

def init_players():
    players = set_players()
    cur_player_index = random.randint(0, len(players)-1)
    cur_player = players[cur_player_index]
    return players, cur_player, cur_player_index

class Player:
    def __init__(self, name=''):
        self.name = name  # default ''
        self.total_points = 0  # Total points for all rounds
        self.round_points = 0  # Points for a single round
    def save_points(self):
        self.total_points += self.round_points
        self.round_points = 0

# ---- Game logic methods --------------

def roll(cur_player_index, cur_player, players, override):
    if override == 0:
        point = random.randint(1, 6)
    else:
        point = override
    if point == 1:
        cur_player.round_points = 0
        return (*change_player(cur_player_index, players), point)
    if point != 1:
        cur_player.round_points += point
        return cur_player_index, cur_player, point

def next(cur_player_index, cur_player, players):
    cur_player.save_points()
    return change_player(cur_player_index, players)

def change_player(cur_player_index, players):
    new_cur_player_index = (cur_player_index+1)%(len(players))
    new_cur_player = players[new_cur_player_index]
    return new_cur_player_index, new_cur_player

def win_check(cur_player, win_points):
    if (cur_player.total_points + cur_player.round_points >= win_points):
        return True
    return False

# ---- IO Methods --------------

def welcome_msg(win_pts):
    print("Welcome to PIG!")
    print(f"First player to get {win_pts} points will win!")
    print("Commands are: r = roll , n = next, q = quit")

def status_msg(players):
    print("Points: ")
    for player in players:
        print(f"\t{player.name} = {player.total_points} ")

def round_msg(result, player):
    if result > 1:
        print(f"Got {result} running total are {player.round_points}")
    else:
        print("Got 1 lost it all!")

def game_over_msg(player, aborted):
    if aborted:
        print("Aborted")
    else:
        print(f"Game over! Winner is player {player.name} with {player.total_points + player.round_points} points")

def input_error(input):
    print(f"{input} is not a viable command, please try again!")

def get_player_choice(player):
    return input(f"Player is {player.name} > ")

def set_players():
    players = []
    players_amount_input = input("Enter the number of players > ")
    while not players_amount_input.isnumeric():
        print("invalid number, please try again")
        players_amount_input = input("Enter the number of players > ")
    players_amount = int(players_amount_input)
    for i in range(players_amount):
        name = input(f"Enter name for player {i + 1} > ")
        players.append(Player(name=name))
    return players

# ----- Testing -----------------
# Here you run your tests i.e. call your game logic methods
# to see that they really work (IO methods not tested here)

def test():
    test_players = [Player("a"), Player("b"), Player("c")]
    p_int = 0
    player = test_players[p_int]

    p_int, player = roll(p_int, player, test_players, 1)
    print(p_int == 1)

    testvalue = 4
    print(testvalue == roll(p_int, player, test_players, testvalue)[2])

    testvalue = player
    p_int, player = next(p_int, test_players[0], test_players)
    print(testvalue != player)

    testvalue = player
    p_int, player = change_player(p_int, test_players)
    print(testvalue != player)

    p_int, player = change_player(p_int, test_players)

    print(win_check(player, 4))



if __name__ == "__main__":
    run()
    # test()