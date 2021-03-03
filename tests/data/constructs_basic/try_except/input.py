
try:
	print('t1', 'try')
except:
	print('t1', 'except')

try:
	1 // 0
	print('t2', 'try')
except:
	print('t2', 'except')

try:
	1 // 0
	print('t3', 'try')
except:
	print('t3', 'except')
finally:
	print('t3', 'finally')

try:
	print('t4', 'try')
except:
	print('t4', 'except')
else:
	print('t4', 'else')
finally:
	print('t4', 'finally')
