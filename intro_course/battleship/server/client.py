from packet import Packet
from events import events
from copy import deepcopy
from uid import uid

class Player:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.id = uid.id()
        self.received_data = Packet()
        self.received_buffer = []
        self.data_buffer_size = 4096
        self.connected = True
        self.username = ""
        self.game_name = None
    
    def send(self, packet):
        self.conn.send(packet)
    
    def close(self):
        self.conn.close()
    
    def receive(self):
        try:
            self.received_buffer = self.conn.recv(self.data_buffer_size)
            byteLength = len(self.received_buffer)
            if byteLength <= 0:
                self.connected = False
                return;
            data = deepcopy(self.received_buffer)
            self.received_data.reset(self.handle_data(data))
        except Exception as ex:
            print(f"Error receiving TCP data: {ex}")
            self.connected = False

    def handle_data(self, data):
        packetLength = 0

        self.received_data.set_bytes(data)

        if self.received_data.unread_length() >= 4:
            packetLength = self.received_data.read_int()
            if packetLength <= 0:
                return True

        while packetLength > 0 and packetLength <= self.received_data.unread_length():
            packetBytes = self.received_data.read_bytes(packetLength)
            
            with (Packet(data=packetBytes)) as packet:
                packetId = packet.read_int()
                events.post("handle packet", packetId, packet)

            packetLength = 0;
            if self.received_data.unread_length() >= 4:
                packetLength = self.received_data.read_int()
                if packetLength <= 0:
                    return True

        if packetLength <= 1:
            return True

        return False
