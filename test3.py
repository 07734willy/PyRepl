import sys

def tracefunc(frame, event, arg):
	if event == "line":
		print(frame)
		
	return tracefunc

class Prompt:
	def __init__(self):
		self.lineno = 0

	def __str__(self):
		self.lineno += 1
		return FakeStr(f"{self.lineno}\n")

PROMPT = Prompt()

sys.ps2 = PROMPT
sys.ps1 = ""



