import re
a = input()
b = "ab"
x = re.findall(b, a)
print(len(x))
print(x)