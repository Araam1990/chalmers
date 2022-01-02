from packet import Packet

class Sender:
    def __init__(self, players):
        self.players = players

        self.packet_names = {
            "dud": self.dud_packet,
            "give id": self.give_id,
            "invalid game name": self.invalid_game_name,
            "game created": self.game_created,
            "game does not exist": self.no_game,
            "game is full": self.game_full,
            "opponent left": self.opponent_left,
            "is host": self.is_host,
            "joined game": self.joined_game,
            "player joined": self.player_joined,
            "username being used": self.username_being_used
        }

        self.packet_ids = {
            self.dud_packet: 0,
            self.give_id: 1,
            self.invalid_game_name: 2,
            self.game_created: 3,
            self.no_game: 4,
            self.game_full: 5,
            self.opponent_left: 6,
            self.is_host: 7,
            self.joined_game: 8,
            self.player_joined: 9,
            self.username_being_used: 10,
        }

    def get_player(self, id):
        for player in self.players:
            if player.id == id:
                return player

    def send_to_one(self, packet_name, id, packet_args=[]):
        packet = self.get_packet(packet_name, packet_args)
        player = self.get_player(id)
        player.send(packet)

    def send_to_all_but_one(self, packet_name, id, packet_args=[]):
        packet = self.get_packet(packet_name, packet_args)
        for player in self.players:
            if player.id != id:
                player.send(packet)

    def send_to_all(self, packet_name, packet_args=[]):
        packet = self.get_packet(packet_name, packet_args)
        for player in self.players:
            player.send(packet)

    def get_packet(self, packet_name, packet_args):
        return self.packet_names[packet_name](*packet_args)

    def dud_packet(self):
        packet = Packet(id=self.packet_ids[self.dud_packet])
        return packet.send()

    def give_id(self, id):
        packet = Packet(id=self.packet_ids[self.give_id])
        packet.write_int(id)
        return packet.send()

    def invalid_game_name(self):
        packet = Packet(id=self.packet_ids[self.invalid_game_name])
        return packet.send()

    def game_created(self, name, is_host, players):
        packet = Packet(id=self.packet_ids[self.game_created])
        packet.write_string(name)
        packet.write_bool(is_host)
        names_list = [player.username for player in players]
        packet.write_list_string(names_list)
        return packet.send()

    def no_game(self):
        packet = Packet(id=self.packet_ids[self.no_game])
        return packet.send()

    def game_full(self):
        packet = Packet(id=self.packet_ids[self.game_full])
        return packet.send()

    def opponent_left(self):
        packet = Packet(id=self.packet_ids[self.opponent_left])
        return packet.send()

    def is_host(self):
        packet = Packet(id=self.packet_ids[self.is_host])
        return packet.send()

    def joined_game(self, name, is_host, players):
        packet = Packet(id=self.packet_ids[self.joined_game])
        packet.write_string(name)
        packet.write_bool(is_host)
        names_list = [player.username for player in players]
        packet.write_list_string(names_list)
        return packet.send()

    def player_joined(self, username):
        packet = Packet(id=self.packet_ids[self.player_joined])
        packet.write_string(username)
        return packet.send()

    def username_being_used(self):
        packet = Packet(id=self.packet_ids[self.username_being_used])
        return packet.send()
