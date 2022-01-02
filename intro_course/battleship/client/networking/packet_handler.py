from struct import pack
from networking.packet import Packet
from components.events import events
from components.player import Player
from networking.packet_sender import Sender

class Handler:
    def __init__(self, sender, client):
        self.sender = sender
        self.client = client
        self.packets = {
            0: self.dud_packet,
            1: self.welcome,
            2: self.invalid_room_name,
            3: self.room_created,
            4: self.no_room,
            5: self.room_full,
            6: self.opponent_left,
            7: self.is_host,
            8: self.joined_game,
            9: self.player_joined,
            10: self.username_being_used
        }

        events.sub("handle packet", self.handle_packet)
    
    def get_player(self, id):
        for player in self.players:
            if player.id == id:
                return player

    def handle_packet(self, packet_id, packet):
        self.packets[packet_id](packet)

    def dud_packet(self, packet: Packet):
        return

    def welcome(self, packet: Packet):
        self.client.id = packet.read_int()

    def invalid_room_name(self, packet: Packet):
        events.post("invalid room name")

    def room_created(self, packet: Packet):
        name = packet.read_string()
        is_host = packet.read_bool()
        players = packet.read_list_string()
        events.post("game lobby", name, is_host, players)
    
    def no_room(self, packet: Packet):
        events.post("no room")

    def room_full(self, packet: Packet):
        events.post("room full")

    def opponent_left(self, packet: Packet):
        events.post("opponent left")

    def is_host(self, packet: Packet):
        events.post("is host")

    def joined_game(self, packet: Packet):
        name = packet.read_string()
        is_host = packet.read_bool()
        players = packet.read_list_string()
        events.post("game lobby", name, is_host, players)

    def player_joined(self, packet: Packet):
        username = packet.read_string()
        events.post("player joined", username)

    def username_being_used(self, packet: Packet):
        events.post("username already used")
