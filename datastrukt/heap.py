from abc import ABC

class Heap:
    def __init__(self, in_list, ordering, key):
        self._inner_list = []
        self._key = key
        self._ordering = ordering
        if in_list:
            for el in in_list:
                self.push(el)
    
    def __repr__(self):
        return f"{self._inner_list}"

    def __len__(self) -> int:
        return len(self._inner_list)

    def __iter__(self):
        iterable = Heap(self._inner_list, self._ordering, self._key)
        return iterable

    def __next__(iterable):
        if len(iterable) > 0:
            return iterable.pop()
        else:
            raise StopIteration

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

class HeapWrapper(ABC):
    def __init__(self, in_list, ordering, key):
        self._heap = Heap(in_list, ordering, key)

    def __repr__(self):
        return repr(self._heap)

    def __len__(self):
        return len(self._heap)

    def __iter__(self):
        return iter(self._heap)

    def __next__(iterable):
        return next(iterable)

    def peek(self):
        return self._heap.peek()
    
    def pop(self):
        return self._heap.pop()
    
    def push(self, el):
        self._heap.push(el)

class MinHeap(HeapWrapper):
    def __init__(self, in_list=None, key=lambda x:x):
        super().__init__(in_list, lambda el1, el2: el1 < el2, key)

class MaxHeap(HeapWrapper):
    def __init__(self, in_list=None, key=lambda x:x):
        super().__init__(in_list, lambda el1, el2: el1 > el2, key)

if __name__ == "__main__":
    nums = [3,5,7,9,7,65,3,2,0]
    heap = MinHeap(nums)
    
    for num in heap:
        print(num)
    
    print(heap)