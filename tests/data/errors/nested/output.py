
try:
	1 // 0
except:
	raise Exception("Inner Exception")
# error: Traceback (most recent call last):
# error:   File "<string>", line 3, in <module>
# error: ZeroDivisionError: integer division or modulo by zero
# error: 
# error: During handling of the above exception, another exception occurred:
# error: 
# error: Traceback (most recent call last):
# error:   File "<string>", line 5, in <module>
# error: Exception: Inner Exception



def call1():
	call2()

def call2():
	call3()

def call3():
	raise Exception("Nested Exception")

call1()
# error: Traceback (most recent call last):
# error:   File "<string>", line 27, in <module>
# error:   File "<string>", line 19, in call1
# error:   File "<string>", line 22, in call2
# error:   File "<string>", line 25, in call3
# error: Exception: Nested Exception
