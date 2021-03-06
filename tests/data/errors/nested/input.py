
try:
	1 // 0
except:
	raise Exception("Inner Exception")



def call1():
	call2()

def call2():
	call3()

def call3():
	raise Exception("Nested Exception")

call1()
