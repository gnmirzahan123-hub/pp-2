import re

x=input()
n=re.search("^Hello", x)
if n:
    print("Yes")
else:
    print("No")    