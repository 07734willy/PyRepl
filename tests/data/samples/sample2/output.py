
x = 2
y = 3
x
# out: 2
y
# out: 3

z = 4
z
# out: 4

q =
# error:   File "<string>", line 13
# error:     q =
# error:        ^
# error: SyntaxError: invalid syntax

x = 2
x
# out: 2

a = b = c = 1
if a:
	if b:
		if c:
			c = 2
			z =
			d = 3
			e = 3
# error:   File "<string>", line 28
# error:     			z =
# error:     			   ^
# error: SyntaxError: invalid syntax
c
# out: 1

z = 5



if x:
	print(20)
elif y:
	y = 30
# out: 20
if z:
	print(21)
# out: 21
'''
foo
bar
'''
# out: '\nfoo\nbar\n'
x
# out: 2
y
# out: 3
z
# out: 5

if x:
	print(10)
# out: 10
4 + \
	2 + \
	3
# out: 9

x
# out: 2
y
# out: 3


# test





