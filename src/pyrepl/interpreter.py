from textwrap import indent
from traceback import format_exception
from contextlib import suppress
import sys

from .fdio import read_fd, write_fd, append_fd, clear_fd
from .segments import get_segments


def strip_newline(text):
	if text.endswith("\n"):
		return text[:-1]
	return text


class Interpreter:
	def __init__(self, fdin, fdout, fderr):
		self.fdin = fdin
		self.fdout = fdout
		self.fderr = fderr

	def process_output(self, offset):
		output = read_fd(self.fdout)
		errput = read_fd(self.fderr)

		def put_data(data, label):
			if not data:
				return

			lineno = self.lineno + offset
			pydata = indent(data, f"# {label}: ", lambda line: True)
			clean_data = strip_newline(pydata)
			self.lines[lineno] = clean_data

			self.lineno += clean_data.count("\n") + 1

			if not data.endswith("\n"):
				lineno = self.lineno + offset
				self.lines[lineno] = "# info: missing trailing newline"
				self.lineno += 1

		put_data(output, "out")
		put_data(errput, "error")

		clear_fd(self.fdout)
		clear_fd(self.fderr)

	def prompt_input(self, offset):
		lineno = self.lineno + offset
		self.lines[lineno] = "# in: "
		self.lineno += 1

	def reset(self):
		self.lineno = 0
		self.lines = {}

		self.global_ns = {}

		clear_fd(self.fdin)
		clear_fd(self.fdout)
		clear_fd(self.fderr)

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
				result = eval(code, self.global_ns)
				self.global_ns['_'] = result

				if result is not None:
					append_fd(self.fdout, repr(result) + "\n")
				return

			exec(code, self.global_ns)
		except EOFError:
			self.prompt_input(offset)
			append_fd(self.fdout, "\n")
			self.write_exc()
		except Exception:
			self.write_exc()

	def write_exc(self):
		etype, value, tb = sys.exc_info()
		exc = "".join(format_exception(etype, value, tb.tb_next))
		append_fd(self.fderr, exc)

	@property
	def output(self):
		return list(self.lines.items())
