from networking.packet import Packet

class Sender:
    def __init__(self, conn):
        self.conn = conn

        self.packet_names = {
            "dud": self.dud_packet,
            "host game": self.host_game,
            "join game": self.join_game,
            "leave room": self.leave_room,
            "start game": self.start_game,
        }

        self.packets = {
            self.dud_packet: 0,
            self.host_game: 1,
            self.join_game: 2,
            self.leave_room: 3,
            self.start_game: 4,
        }

    def send(self, packet_name, packet_args):
        self.conn.send(self.packet_names[packet_name](*packet_args))

    def dud_packet(self, id):
        packet = Packet(id=self.packets[self.dud_packet])
        packet.write_int(id)
        return packet.send()

    def host_game(self, id, room_name, username):
        packet = Packet(id=self.packets[self.host_game])
        packet.write_int(id)
        packet.write_string(room_name)
        packet.write_string(username)
        return packet.send()

    def join_game(self, id, room_name, username):
        packet = Packet(id=self.packets[self.join_game])
        packet.write_int(id)
        packet.write_string(room_name)
        packet.write_string(username)
        return packet.send()

    def leave_room(self, user_id):
        packet = Packet(id=self.packets[self.leave_room])
        packet.write_int(user_id)
        return packet.send()

    def start_game(self, user_id):
        packet = Packet(id=self.packets[self.start_game])
        packet.write_int(user_id)
        return packet.send()
