import re
a=input()
b=input()
c=re.search(re.escape(b),a)
if c:
    print("Yes")
else:
    print("No")