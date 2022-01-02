import socket
from _thread import *
from packet_sender import Sender
from packet_handler import Handler
from client import Player

class Server:
    def __init__(self):
        self.games = []
        self.players = []

        self.sender = Sender(self.players)
        self.handler = Handler(self.games, self.players)

    def threaded_client(self, player):
        self.sender.send_to_one("give id", player.id, [player.id])

        while player.connected:
            try:
                player.receive()
            except:
                player.connected = False

        print("Lost connection")
        player.close()

        for game_i in range(len(self.games)):
            if self.games[game_i].name == player.game_name:
                game = self.games[game_i]

                if len(game.players) == 1:
                    self.games.pop(game_i)
                    break

                if game.players[0].id == player.id:
                    game.players.pop(0)
                elif game.players[1].id == player.id:
                    game.players.pop(1)

                self.sender.send_to_one("opponent left", game.players[0].id)
                
                break

        index = -1
        for i in range(len(self.players)):
            if self.players[i].id == player.id:
                index = i
                break
        if index >= 0:
            self.players.pop(index)

    def start(self):
        server = ""
        port = 3000

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server, port))
        except socket.error as e:
            print(e)

        s.listen(2)
        print(f"Server Started, listening to port {port}")

        while True:
            conn, addr = s.accept()
            print("Connected to:", addr)

            player = Player(conn, addr)
            self.players.append(player)

            start_new_thread(self.threaded_client, (player,))

server = Server()
server.start()