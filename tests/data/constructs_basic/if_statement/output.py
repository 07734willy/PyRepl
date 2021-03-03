
if True:
	print(3)
# out: 3

if False:
	print(2)


if False:
	print(4)
else:
	print(5)
# out: 5


if False:
	print('foo')
elif False:
	print('fizz')
elif True:
	print('buzz')
else:
	print('bar')
# out: buzz
