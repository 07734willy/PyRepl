from textwrap import indent
from string import ascii_letters
from random import choices
from atexit import register
from io import StringIO
from json import dump
import sys

class Prompt:
	def __init__(self):
		self.lineno = 0
		self.outputs = {}

		self.prompt = f":{choices(ascii_letters, k=7)}"
		
		sys.stdout = sys.stderr = self.buffer = StringIO()

	def __str__(self):
		output = self.buffer.getvalue()
		size, thunk = self.deprompt(output)

		with open("debug.txt", "a") as f:
			f.write(output)
			f.write("|||>")

		if thunk:
			pyoutput = indent(thunk, f"# out[{self.lineno}]: ")
			self.outputs[self.lineno] = pyoutput
		
		self.buffer.truncate(0)
		self.buffer.seek(0)

		self.lineno += size
		return self.prompt

	def dump(self):
		data = list(self.outputs.items())[::-1]
		sys.__stdout__.write('\n')
		dump(data, sys.__stdout__)

	def deprompt(self, text):
		if not text.startswith(self.prompt):
			return 0, text

		subtext = text[len(self.prompt):]
		size, thunk = self.deprompt(subtext)
		return size + 1, thunk

PROMPT = Prompt()

sys.ps1 = PROMPT
sys.ps2 = PROMPT.prompt

register(PROMPT.dump)

# TODO cleanup namespace
