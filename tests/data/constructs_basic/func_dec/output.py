
def foo():
	x = 1
	return x

foo()
# out: 1

def bar():
	def inner():
		return 'test'
	return inner()

bar()
# out: 'test'


def add(x, y):
	return x + y

add(1, 2)
# out: 3


def max_(*args):
	return max(*args)

max(1, 2, 3)
# out: 3

def defaulted(key=5):
	return key

defaulted()
# out: 5
