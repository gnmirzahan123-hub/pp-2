n = int(input())

if n <= 0:
    print("NO")
else:
    while n > 1:
        if n % 2 != 0:
            print("NO")
            break
        n //= 2
    else:
        print("YES")