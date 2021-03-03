from textwrap import indent
from traceback import format_exception
from contextlib import suppress
import sys

from .fdio import read_fd, write_fd, append_fd, clear_fd
from .parser import get_segments

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
			pyoutput = indent(output, "# out: ", lambda line: True)
			clean_output = strip_newline(pyoutput)
			self.lines[lineno] = clean_output

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
		code = code + "\n\n"

		segments = get_segments(code)
		for segment in segments:
			data_input = segment.parse_input()
			
			clear_fd(self.fdin)
			write_fd(self.fdin, data_input)

			self.eval_segment(segment.code, segment.offset)
			self.process_output(segment.offset)

			self.lineno += segment.numlines

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

