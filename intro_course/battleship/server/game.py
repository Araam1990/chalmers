from uid import uid

class Game:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.turn = 0
        self.player_maps = []
        self.player_hit_maps = []
        self.state = "Lobby"