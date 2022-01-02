class UID:
    def __init__(self):
        self.__id = 0

    def id(self):
        self.__id += 1
        return self.__id

uid = UID()