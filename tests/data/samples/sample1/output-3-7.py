
x = 2

y = 3
z = 3
x
# out: 2
y
# out: 3

if x:

	x = 55
	print(x)

	x = 66
	print(x)

else:
	x = 77
	print(x)
# out: 55
# out: 66

x = 1
while x:

	if x:
		z = 2
		print(z)

	elif x < 2:

		z = 4
		print(z)
	z += 2
	print(z)

	x = 0
# out: 2
# out: 4

x = 3

[

	2,

3

]
# out: [2, 3]

'''

if x:
	x

if y:

	y
'''
# out: '\n\nif x:\n\tx\n\nif y:\n\n\ty\n'

x = 3

if x:
	x = 2
	print(x)
# out: 2
while x:
	break

x = 2
if x:
	print(x)
	z = 2

	y = 
	z
else:
	print(x)
	x
# out:   File "<string>", line 79
# out:     y =
# out:        ^
# out: SyntaxError: invalid syntax

x
# out: 2
x = 4

