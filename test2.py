import sys

class FakeStr:
	def __init__(self, text):
		self.text = text

	def __add__(self, other):
		print("///////")
		return self.text + other

	def __radd__(self, other):
		print("+++++++")
		return other + self.text

	def __repr__(self):
		print("&&&&&&&&&")
		return self.text

	def __str__(self):
		print("~~~~~~~")
		return self.text



names = ['__add__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__']

def makename(name):
	def func(*x):
		print('called', name, 'with', *x)

	return func

for name in names:
	setattr(FakeStr, name, makename(name))


class Faker(str):
	def __str__(self):
		...

class Prompt:
	def __init__(self):
		self.lineno = 0

	def __str__(self):
		self.lineno += 1
		return FakeStr(f"{self.lineno}\n")

PROMPT = Prompt()

sys.ps2 = PROMPT
sys.ps1 = ""
