n = int(input())
numbers = list(map(int, input().split()))

maximum = numbers[0]
for x in numbers:
    if x > maximum:
        maximum = x

print(maximum)