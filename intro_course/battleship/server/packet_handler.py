from packet import Packet
from packet_sender import Sender
from events import events
from game import Game

class Handler:
    def __init__(self, games, players):
        self.games = games
        self.players = players
        self.sender = Sender(self.players)

        self.packet_ids = {
            0: self.dud_packet,
            1: self.create_lobby,
            2: self.join_game,
            3: self.leave_game,
            4: self.start_game,
        }

        events.sub("handle packet", self.handle_packet)
    
    def get_player(self, id):
        for player in self.players:
            if player.id == id:
                return player
        return False

    def get_game(self, name):
        for game in self.games:
            if game.name == name:
                return game
        return False

    def handle_packet(self, packet_id, packet):
        self.packet_ids[packet_id](packet)

    def dud_packet(self, packet: Packet):
        id = packet.read_int()
        self.sender.send_to_one("dud", id)

    def create_lobby(self, packet: Packet):
        id = packet.read_int()
        game_name = packet.read_string()
        username = packet.read_string()
        if self.get_game(game_name):
            self.sender.send_to_one("invalid game name", id)
            return
        player = self.get_player(id)
        player.username = username
        game = Game(game_name)
        game.players.append(player)
        player.game_name = game.name
        self.games.append(game)
        self.sender.send_to_one("game created", id, [game.name, (game.players[0].id == player.id), game.players])

    def join_game(self, packet: Packet):
        id = packet.read_int()
        game_name = packet.read_string()
        game = self.get_game(game_name)
        if not game:
            self.sender.send_to_one("game does not exist", id)
            return
        if len(game.players) == 2:
            self.sender.send_to_one("game is full", id)
            return
        username = packet.read_string()
        if username in [player.username for player in game.players]:
            self.sender.send_to_one("username being used", id)
            return
        player = self.get_player(id)
        player.username = username
        game.players.append(player)
        player.game_name = game.name
        self.sender.send_to_one("player joined", game.players[0].id, [player.username])
        self.sender.send_to_one("joined game", id, [game.name, (game.players[0].id == player.id), game.players])

    def leave_game(self, packet: Packet):
        user_id = packet.read_int()
        player = self.get_player(user_id)
        game = self.get_game(player.game_name)
        if not game:
            return
        if len(game.players) == 1:
            for i in range(len(self.games)):
                if self.games[i].name == game.name:
                    self.games.pop(i)
                    return

        if game.players[0].id == player.id:
            self.sender.send_to_one("is host", game.players[1].id)
            game.players.pop(0)
        elif game.players[1].id == player.id:
            game.players.pop(1)
        self.sender.send_to_one("opponent left", game.players[0].id)

    def start_game(self, packet: Packet):
        user_id = packet.read_int()
        player = self.get_player(user_id)
        game = self.get_game(player.game_name)
        game.state = "Placements"w
