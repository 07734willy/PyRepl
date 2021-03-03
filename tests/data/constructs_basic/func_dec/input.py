
def foo():
	x = 1
	return x

foo()

def bar():
	def inner():
		return 'test'
	return inner()

bar()


def add(x, y):
	return x + y

add(1, 2)


def max_(*args):
	return max(*args)

max(1, 2, 3)

def defaulted(key=5):
	return key

defaulted()
