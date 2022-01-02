import struct
import traceback
import pygame

class Packet:

    def __init__(self, id = None, data = None):
        self.readPos = 0
        self.buffer = bytearray()

        if id != None:
            self.write_id(id)
        if data != None:
            self.set_data(data)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)

    def write_id(self, id):
        self.write_int(id)

    def set_data(self, data):
        self.set_bytes(data)

    def set_bytes(self, data):
        self.write_bytelist(data)
        self.readableBuffer = self.buffer

    def write_length(self):
        self.insert_int(len(self.buffer))

    def insert_int(self, value):
        self.buffer = value.to_bytes(4, "big", signed=True) + self.buffer

    def to_array(self):
        readableBuffer = self.buffer
        return readableBuffer

    def length(self):
        return len(self.buffer); 

    def unread_length(self):
        return self.length() - self.readPos

    def reset(self, reset = True):
        if reset:
            self.buffer = bytearray()
            self.readableBuffer = None
            self.readPos = 0
        else:
            self.readPos -= 4

    def send(self):
        self.write_length()
        return self.buffer

    def write_byte(self, value):
        self.buffer.append(value)

    def write_bytelist(self, value):
        self.buffer += value
    
    def write_short(self, value):
        self.buffer += value.to_bytes(2, "big", signed=True)
    
    def write_int(self, value):
        self.buffer += value.to_bytes(4, "big", signed=True)
    
    def write_long(self, value):
        self.buffer += value.to_bytes(8, "big", signed=True)
    
    def write_float(self, value):
        self.buffer += bytearray(struct.pack("f", value))
    
    def write_bool(self, value):
        self.buffer += bytes([value])
    
    def write_string(self, value):
        self.write_int(len(value))
        self.buffer += value.encode()
    
    def write_vector2(self, value):
        self.write_float(value.x)
        self.write_float(value.y)
    
    def write_list_string(self, value):
        self.write_int(len(value))
        for string in value:
            self.write_string(string)
    
    def read_byte(self, moveReadPos = True):
        if len(self.buffer) > self.readPos:
            value = self.buffer[self.readPos]
            if moveReadPos:
                self.readPos += 1
            return value
        else:
            raise(Exception("Could not read value of type 'byte'!"))

    def read_bytes(self, length, moveReadPos = True):
        if len(self.buffer) > self.readPos:
            value = self.buffer[self.readPos : self.readPos + length]
            if moveReadPos:
                self.readPos += length
            return value
        else:
            raise(Exception("Could not read value of type 'byte[]'!"))

    def read_short(self, moveReadPos = True):
        if len(self.buffer) > self.readPos:
            value = self.buffer[self.readPos : self.readPos + 2]
            value = int.from_bytes(value, "big", signed=True)
            if moveReadPos:
                self.readPos += 2
            return value
        else:
            raise(Exception("Could not read value of type 'short'!"))

    def read_int(self, moveReadPos = True):
        if len(self.buffer) > self.readPos:
            value = self.buffer[self.readPos : self.readPos + 4]
            value = int.from_bytes(value, "big", signed=True)
            if moveReadPos:
                self.readPos += 4
            return value
        else:
            raise(Exception("Could not read value of type 'int'!"))

    def read_long(self, moveReadPos = True):
        if len(self.buffer) > self.readPos:
            value = self.buffer[self.readPos : self.readPos + 8]
            value = int.from_bytes(value, "big", signed=True)
            if moveReadPos:
                self.readPos += 8
            return value
        else:
            raise(Exception("Could not read value of type 'long'!"))

    def read_float(self, moveReadPos = True):
        if len(self.buffer) > self.readPos:
            value = self.buffer[self.readPos : self.readPos + 4]
            value = struct.unpack("f", value)
            if moveReadPos:
                self.readPos += 4
            return value[0]
        else:
            raise(Exception("Could not read value of type 'float'!"))

    def read_bool(self, moveReadPos = True):
        if len(self.buffer) > self.readPos:
            value = self.buffer[self.readPos]
            if moveReadPos:
                self.readPos += 1
            return bool(value)
        else:
            raise(Exception("Could not read value of type 'bool'!"))

    def read_string(self, moveReadPos = True):
        try:
            length = self.read_int()
            value = self.buffer[self.readPos : self.readPos + length]
            value = value.decode()
            if moveReadPos and len(value) > 0:
                self.readPos += length
            return value
        except:
            raise(Exception("Could not read value of type 'string'!"))

    def read_vector2(self, moveReadPos = True):
        return pygame.Vector2(self.read_float(moveReadPos), self.read_float(moveReadPos))

    def read_list_string(self, moveReadPos = True):
        length = self.read_int()
        list = []
        for _ in range(length):
            list.append(self.read_string())
        return list
    