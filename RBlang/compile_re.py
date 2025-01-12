import re

t = "PlayerInventory.add(parameter1, parameter2)"
pattern = r"(?P<before_parentheses>.*)\((?P<inside_parentheses>.*)\)"
r = re.match(pattern, t)

if r:
    print("괄호 앞부분:", r.group("before_parentheses"))
    print("괄호 안 내용:", r.group("inside_parentheses"))
else:
    print("No match found")



