from contextlib import suppress
from codeop import CommandCompiler
from functools import lru_cache
import ast

from logging import getLogger
logger = getLogger(__name__)


class Parser:
	def __init__(self):
		self._exec_error = None
		self.exec_error_cached = False
		self.compiler = CommandCompiler()
		self.line_offset = 0

	def get_parse_error(self, code, mode):
		try:
			self.parse_code(code, mode)
		except SyntaxError as error:
			return error

	@lru_cache(maxsize=1)
	def get_parse_single_error(self, code):
		return self.get_parse_error(code, "single")

	def update_offset(self, consumed_code):
		self.line_offset += consumed_code.count("\n")

	def get_parse_exec_error(self, code):
		logger.info("Parsing exec-error")
		if not self.exec_error_cached:
			logger.info("Missed exec-error cache")
			self._exec_error = self.get_parse_error(code, "exec")
			self.line_offset = 0
			self.exec_error_cached = True

		if self._exec_error is None:
			logger.info("No exec-error")
			return None

		# python 3.10.x - extra arguments added to SyntaxError:
		#  'end_lineno' and 'end_offset'
		msg, (filename, lineno, offset, text, *extras) = self._exec_error.args
		lineno -= self.line_offset
		details = (filename, lineno, offset, text, *extras)

		error = type(self._exec_error)(msg, details)
		return error

	def compare_single_and_exec(self, code):
		logger.info("compiling single + exec")
		error_single = self.get_parse_single_error(code)
		error_exec = self.get_parse_exec_error(code)

		errors_equal = compare_exceptions(error_single, error_exec)
		if errors_equal:
			self.exec_error_cached = False

		return errors_equal

	@lru_cache(maxsize=128)
	def parse_code(self, code, mode="single"):
		return compile(code, "<file>", mode, flags=ast.PyCF_ONLY_AST)

	def is_valid_segment_start(self, line):
		if not self.is_functional(line):
			return False

		try:
			self.compiler(line, "<file>", "single")
		except (OverflowError, SyntaxError, ValueError):
			return False
		return True

	def is_functional(self, raw_line):
		line = f"{raw_line}\n "
		return self.is_influential(line)

	def is_influential(self, line):
		if is_empty(line):
			return False

		if is_comment(line):
			return False

		with suppress(Exception):
			tree = self.parse_code(line)
			nodes = ast.iter_child_nodes(tree)
			return bool(list(nodes))

		return True


def compare_exception_types(e1, e2):
	return type(e1) == type(e2) and e1.msg == e2.msg


def compare_exceptions(e1, e2):
	if type(e1) != type(e2):
		return False

	if not isinstance(e1, SyntaxError):
		return e1.args == e2.args

	msg1, (fn1, ln1, off1, txt1, *_) = e1.args
	msg2, (fn2, ln2, off2, txt2, *_) = e2.args

	args1 = (msg1, fn1, ln1, off1, txt1)
	args2 = (msg2, fn2, ln2, off2, txt2)

	return args1 == args2


def is_empty(line):
	return not line.strip()


def is_comment(line):
	return line.strip().startswith("#")
