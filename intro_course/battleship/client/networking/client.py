import socket
from copy import deepcopy
from networking.packet import Packet
from networking.packet_handler import Handler
from networking.packet_sender import Sender
from components.events import events

class Client():
    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ""
        self.port = 3000
        self.addr = (self.server, self.port)
        self.received_data = Packet()
        self.received_buffer = []
        self.data_buffer_size = 4096

        self.sender = Sender(self.conn)
        self.handler = Handler(self.sender, self)
        self.id = None
        self.username = ""

        self.connect()

    def connect(self):
        try:
            self.conn.connect(self.addr)
            self.receive()
        except:
            pass

    def send(self, packet_name, packet_args):
        self.sender.send(packet_name, packet_args)
    
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
            self.conn.close()

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

client = Client()