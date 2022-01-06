list = [74,34,65,96,23,87,42,51,11]
pivot = list[0]
left = 1
right = len(list) - 1
while left < right:
    while list[right] > pivot:
        right -= 1
    while list[left] < pivot:
        left += 1
    if right < left:
        list[0], list[right] = list[right], list[0]
    else:
        list[left], list[right] = list[right], list[left]

print(list)