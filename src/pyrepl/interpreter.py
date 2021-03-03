from textwrap import indent
from traceback import format_exception
from contextlib import suppress
import sys
import re

from .fdio import read_fd, write_fd, append_fd, clear_fd

DECOR_LINE  = r"(?:@.*\n)"
SOURCE_LINE = r"(?:.*\n)"
INPUT_LINE  = r"(?:# in: .*\n)"
EMPTY_LINE  = r"(?:\n|#(?! in: ).*\n)"

PRESOURCES = rf"(?:{EMPTY_LINE}|{INPUT_LINE}|{DECOR_LINE})"
SOURCES    = rf"(?:{EMPTY_LINE}|{INPUT_LINE}|{SOURCE_LINE})"
EXT_DATA   = rf"(?:{EMPTY_LINE}|{INPUT_LINE})"
EMPTY      = rf"(?:{EMPTY_LINE})"


def get_syntax_error(code):
	try:
		compile(code, "<string>", "exec")
	except SyntaxError as e:
		return "".join(format_exception(type(e), e, e.__traceback__))

def get_subsegments(code):
	regex = rf"^((({EMPTY}*{PRESOURCES}*{SOURCES}+?){EXT_DATA}*?){EMPTY}*)(?=[^\s#]|$)"
	return re.match(regex, code).groups()

def get_segments(code):
	all_segment, data_segment, code_segment = get_subsegments(code)

	error = get_syntax_error(code_segment)
	new_code = code[len(all_segment):]
	while error and new_code:
		all_next, data_next, code_next = get_subsegments(new_code)
		
		new_error = get_syntax_error(all_segment + code_next)
		if new_error == error:
			#print(new_error, file=sys.__stderr__)
			#print(error, file=sys.__stderr__)
			break
		# import sys
		# print('>>>>>>>>>', file=sys.__stderr__)
		# print(code_segment, file=sys.__stderr__)
		# print('..........', file=sys.__stderr__)
		# print(new_error, file=sys.__stderr__)
		# print(error, file=sys.__stderr__)
		# print('????????', file=sys.__stderr__)
		# print(all_segment + code_next, file=sys.__stderr__)

		error = new_error
		code_segment = all_segment + code_next
		data_segment = all_segment + data_next
		all_segment  = all_segment + all_next
		new_code = code[len(all_segment):]

	return all_segment, data_segment, code_segment
	

def parse_input(data_segment):
	regex = r"# in: (.*\n)"
	matches = re.finditer(regex, data_segment)
	
	data = "".join(match.group(1) for match in matches)
	return data

def strip_newline(text):
	if text.endswith("\n"):
		return text[:-1]
	return text

class Interpreter:
	def __init__(self, fdin, fdout):
		self.fdin = fdin
		self.fdout = fdout

	def process_output(self, offset):
		output = read_fd(self.fdout)

		if output:
			lineno = self.lineno + offset
			clean_output = strip_newline(output)
			pyoutput = indent(clean_output, "# out: ", lambda line: True)
			self.lines[lineno] = pyoutput

			self.lineno += clean_output.count("\n") + 1

			if not output.endswith("\n"):
				lineno = self.lineno + offset
				self.lines[lineno] = f"# warn: Missing trailing newline"
				self.lineno += 1

		clear_fd(self.fdout)

	def prompt_input(self, offset):
		lineno = self.lineno + offset
		self.lines[lineno] = "# in: "
		self.lineno += 1

	def reset(self):
		self.lineno = 0
		self.lines = {}

		self.global_ns = {}
		self.local_ns = {}

		clear_fd(self.fdin)
		clear_fd(self.fdout)

	def eval(self, code):
		self.reset()
		self.code = code + "\n\n"

		while self.code:
			all_segment, data_segment, code_segment = get_segments(self.code)
			data_input = parse_input(data_segment)
			self.code = self.code[len(all_segment):]

			clear_fd(self.fdin)
			write_fd(self.fdin, data_input)

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
					append_fd(self.fdout, repr(result) + "\n")
				return
			
			exec(code, self.global_ns, self.local_ns)
		except EOFError as e:
			self.prompt_input(offset)
			append_fd(self.fdout, "\n")
			self.write_exc()
		except Exception as e:
			self.write_exc()
		finally:
			self.global_ns.update(self.local_ns)

	def write_exc(self):
		etype, value, tb = sys.exc_info()
		exc = "".join(format_exception(etype, value, tb.tb_next))
		append_fd(self.fdout, exc)

	@property
	def output(self):
		return list(self.lines.items())

