
try:
	1 // 0
except:
	raise Exception("Inner Exception")
# out: Traceback (most recent call last):
# out:   File "<string>", line 3, in <module>
# out: ZeroDivisionError: integer division or modulo by zero
# out: 
# out: During handling of the above exception, another exception occurred:
# out: 
# out: Traceback (most recent call last):
# out:   File "<string>", line 5, in <module>
# out: Exception: Inner Exception



def call1():
	call2()

def call2():
	call3()

def call3():
	raise Exception("Nested Exception")

call1()
# out: Traceback (most recent call last):
# out:   File "<string>", line 27, in <module>
# out:   File "<string>", line 19, in call1
# out:   File "<string>", line 22, in call2
# out:   File "<string>", line 25, in call3
# out: Exception: Nested Exception
