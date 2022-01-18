from abc import ABC, abstractclassmethod

class Heap(ABC):
    def __init__(self, key=lambda x:x):
        self._inner_list = []
        self._key = key
    
    def __repr__(self):
        return f"{self._inner_list}"

    def __len__(self) -> int:
        return len(self._inner_list)
    
    @abstractclassmethod
    def _ordering(self, el1, el2):
        pass

    def peek(self):
        return self._inner_list[0]

    def push(self, el):
        self._inner_list.append(el)
        i = len(self._inner_list) - 1
        j = i // 2
        while i > 0 and self._ordering(self._key(self._inner_list[i]), self._key(self._inner_list[j])):
            self._inner_list[i], self._inner_list[j] = self._inner_list[j], self._inner_list[i]
            i, j = j, j // 2

    def pop(self):
        if len(self) == 0:
            raise IndexError("No available value to pop")
        self._inner_list[0], self._inner_list[-1] = self._inner_list[-1], self._inner_list[0]
        el = self._inner_list.pop()
        i, j = 0, 1
        while j < len(self._inner_list):
            if j + 1 < len(self._inner_list) and self._ordering(self._inner_list[j + 1], self._inner_list[j]):
                j += 1
            elif j == len(self._inner_list):
                break
            if self._ordering(self._inner_list[j], self._inner_list[i]):
                self._inner_list[i], self._inner_list[j] = self._inner_list[j], self._inner_list[i]
                i, j = j, j*2+1
            else:
                break
        return el

class MinHeap(Heap):
    def _ordering(self, el1, el2):
        return el1 < el2

class MaxHeap(Heap):
    def _ordering(self, el1, el2):
        return el1 > el2

class Person:
    def __init__(self, age, name):
        self.age = age
        self.name = name
    
    def __repr__(self):
        return f"{self.name}: {self.age}"

class Stack:
    pass

if __name__ == "__main__":
    heap = MinHeap()
    nums = [4,6,8,87,3,2,57,18]
    for num in nums:
        heap.push(num)
        print(heap)
    while heap:
        print(heap.pop())
