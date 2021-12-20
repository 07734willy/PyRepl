from contextlib import suppress
from codeop import CommandCompiler
from functools import lru_cache
import ast


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
		if not self.exec_error_cached:
			self._exec_error = self.get_parse_error(code, "exec")
			self.line_offset = 0
			self.exec_error_cached = True

		if self._exec_error is None:
			return None

		msg, (filename, lineno, offset, text) = self._exec_error.args
		lineno -= self.line_offset
		details = (filename, lineno, offset, text)

		error = type(self._exec_error)(msg, details)
		return error

	def compare_single_and_exec(self, code):
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
	return type(e1) == type(e2) and e1.args == e2.args


def is_empty(line):
	return not line.strip()


def is_comment(line):
	return line.strip().startswith("#")
