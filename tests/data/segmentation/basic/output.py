
x = 2
x
# out: 2
x
# out: 2

y = 3
print(y); z = 4; print(z)
# out: 3
# out: 4
z
# out: 4

y
# out: 3
if y:
	print(y)
	y = 10
# out: 3
y
# out: 10

if y:
	y = 12
	print(y)
elif z:
	print(y)
elif z:
	print(z)
else:
	print(x)
# out: 12
if y:
	y = 13
	print(y)
# out: 13
x
# out: 2


try:
	print('try block')
	raise ValueError()
except ValueError:
	print("except block")
finally:
	print("finally block")
# out: try block
# out: except block
# out: finally block
try:
	print('try block')
except:
	pass
else:
	print("else block")
finally:
	print("finally block")
# out: try block
# out: else block
# out: finally block


if y:
	print(y)
# out: 13
'''
foo
'''
# out: '\nfoo\n'

if z:
	print(y)
# out: 13
"""fizz"""
# out: 'fizz'

if x:
	print(y)
# out: 13
[
2,
3,
]
# out: [2, 3]

if x:
	print(y)
# out: 13
2 \
	+ 4 \
	+ 5
# out: 11


if x:
	print(y)
# out: 13
(2 and 
		3 and
		7)
# out: 7
