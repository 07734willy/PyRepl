

user = input("Username>")
# in: foo
# out: Username>foo

print(f"Your username: {user}")
# out: Your username: foo

lines = []
if True:
	lines.append(input("Line 1:"))
	lines.append(input("Line 2:"))
	lines.append(input("Line 3:"))
# in: a
# in: b
# in: c
# out: Line 1:a
# out: Line 2:b
# out: Line 3:c

print(lines)
# out: ['a', 'b', 'c']

input("This should populate, with an error initially")
# in: 
# out: This should populate, with an error initially
# out: Traceback (most recent call last):
# out:   File "<string>", line 25, in <module>
# out: EOFError: EOF when reading a line

result = input("We're going to attempt to fake the input line in a comment")
  # in: wrong
# in: right
# out: We're going to attempt to fake the input line in a commentright

print(result)
# out: right

