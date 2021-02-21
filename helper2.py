from textwrap import indent
from traceback import print_exc, format_exc, walk_tb, walk_stack, format_exception
from threading import Thread
from contextlib import suppress
from pprint import pformat
from io import StringIO
from json import dump
import sys
import re

SOURCE_LINE = r"(?:.*\n)"
INPUT_LINE = r"(?:# in: .*\n)"
EMPTY_LINE = r"(?:\n|#(?! in: ).*\n)"

SOURCES  = rf"(?:{EMPTY_LINE}|{INPUT_LINE}|{SOURCE_LINE})"
EXT_DATA = rf"(?:{EMPTY_LINE}|{INPUT_LINE})"
EMPTY    = rf"(?:{EMPTY_LINE})"

DEFAULT_TIMEOUT = 1

def get_segments(code):
	regex = rf"^((({EMPTY}*{SOURCES}+?){EXT_DATA}*?){EMPTY}*)(?=[^\s#]|$)"
	return re.match(regex, code).groups()

def parse_input(data_segment):
	regex = r"# in: (.*\n)"
	matches = re.finditer(regex, data_segment)
	
	data = "".join(match.group(1) for match in matches)
	return data

def setfds():
	sys.stdout = sys.stderr = StringIO()
	sys.stdin = StdinIO(sys.stdout)

def reset_fd(fd):
	fd.truncate(0)
	fd.seek(0)

def write_fd(fd, data):
	fd.write(data)
	fd.seek(0)

def debug(*args, **kwargs):
	#print(*args, **kwargs, file=sys.__stdout__)
	...

class StdinIO(StringIO):
	def __init__(self, stdout):
		self.stdout = stdout
		super().__init__()

	def read(self, *args, **kwargs):
		result = super().read(*args, **kwargs)
		self.stdout.write(result)
		return result
	
	def readline(self, *args, **kwargs):
		result = super().readline(*args, **kwargs)
		self.stdout.write(result)
		return result
	
	def readlines(self, *args, **kwargs):
		result = super().readlines(*args, **kwargs)
		self.stdout.writelines(result)
		return result

class Interpeter:
	def __init__(self):
		self.lineno = 0
		self.lines = {}
		
		self.code = sys.stdin.read() + "\n"
		setfds()
		
		self.global_ns = {}
		self.local_ns = {}

	def process_output(self, offset):
		output = sys.stdout.getvalue()
		
		if output:
			lineno = self.lineno + offset
			pyoutput = indent(output, "# out: ", lambda line: True)
			self.lines[lineno] = pyoutput

			self.lineno += output.count("\n")

		reset_fd(sys.stdout)

	def prompt_input(self, offset):
		lineno = self.lineno + offset
		self.lines[lineno] = "# in: "
		self.lineno += 1

	def eval(self):
		while self.code:
			all_segment, data_segment, code_segment = get_segments(self.code)
			data_input = parse_input(data_segment)
			self.code = self.code[len(all_segment):]

			reset_fd(sys.stdin)
			write_fd(sys.stdin, data_input)

			offset = data_segment.count("\n")
			self.eval_segment(code_segment, offset)
			self.process_output(offset)

			self.lineno += all_segment.count("\n")

	def eval_segment(self, code_segment, offset):
		code = "\n" * self.lineno + code_segment
		try:
			with suppress(SyntaxError):
				result = eval(code, self.global_ns, self.local_ns)
				self.local_ns['_'] = result

				if result is not None:
					print(result)
				return
			
			exec(code, self.global_ns, self.local_ns)
		except EOFError as e:
			self.prompt_input(offset)
			sys.stdout.write("\n")
			self.write_exc()
		except Exception as e:
			self.write_exc()

	def write_exc(self):
			etype, value, tb = sys.exc_info()
			exc = "".join(format_exception(etype, value, tb.tb_next))
			print(exc, end="")

	def dump(self):
		data = list(self.lines.items())
		dump(data, sys.__stdout__)

def write_error(msg):
	dump([[-1, msg]], sys.__stdout__)

def main():
	try:
		timeout = float(sys.argv[1])
	except:
		timeout = DEFAULT_TIMEOUT

	interpreter = Interpeter()
	
	thread = Thread(target=interpreter.eval)
	thread.daemon = True
	thread.start()
	thread.join(timeout)

	if not thread.is_alive():
		interpreter.dump()
	else:
		write_error("Error: execution timed out")

if __name__ == "__main__":
	main()
