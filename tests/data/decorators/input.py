
def add1(f):
	def wrapper(*args, **kwargs):
		return f(*args, **kwargs) + 1
	return wrapper


@add1
def ret7():
	return 7

ret7()

@add1
@add1
@add1
@add1
def ret1():
	return 1

ret1()

def addn(n):
	def decorator(f):
		def wrapper(*args, **kwargs):
			return f(*args, **kwargs) + n
		return wrapper
	return decorator

@addn(5)
def ret4():
	return 4

ret4()
