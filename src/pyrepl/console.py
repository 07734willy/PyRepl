from code import InteractiveConsole
from contextlib import suppress
from itertools import chain
import ast
import sys


def profile(func):
	return func


class Compile:
	def __init__(self, compiler):
		self.flags = compiler.flags | ast.PyCF_ONLY_AST

	def __call__(self, source, filename, symbol):
		return compile(source, filename, symbol, self.flags, True)


class DryRunConsole(InteractiveConsole):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.compile.compiler = Compile(self.compile.compiler)

		self.error = None
		self.codeobj = None

	@profile
	def runsource(self, source, filename="<input>", symbol="single"):
		self.codeobj = None
		try:
			self.codeobj = self.compile(source, filename, symbol)
			return self.codeobj is None
		except (OverflowError, SyntaxError, ValueError):
			self.showsyntaxerror(filename)
			return False

	@profile
	def push(self, line, optimize=True):
		retval = super().push(line)
		if optimize:
			self.optimize_buffer()
		return retval

	@profile
	def clone(self):
		console = DryRunConsole()
		console.buffer = list(self.buffer)
		return console

	@profile
	def optimize_buffer(self):
		if not self.buffer:
			return

		last_line = self.buffer[-1]
		last_line_influencial = is_influential(last_line)

		if len(self.buffer) >= 2:
			penultimate_line_influential = is_influential(self.buffer[-2])
			if not last_line_influencial and not penultimate_line_influential:
				del self.buffer[-1]
				return

		if not last_line_influencial:
			return

		if len(self.buffer) < 8:
			return

		console = self.clone()
		pending = console.push("", optimize=False)
		if pending or console.error:
			return

		"""
		print("Optimized buffer from:", file=sys.stderr)
		print("-" * 40, file=sys.stderr)
		print("\n".join(self.buffer), file=sys.stderr)
		print("-" * 40, file=sys.stderr)
		"""

		deletion_ranges = list(get_deletion_ranges(console.codeobj))
		for begin_lineno, end_lineno in deletion_ranges[::-1]:
			del self.buffer[begin_lineno:end_lineno]

		"""
		print("To new buffer:", file=sys.stderr)
		print("-" * 40, file=sys.stderr)
		print("\n".join(self.buffer), file=sys.stderr)
		print("-" * 40, file=sys.stderr)
		"""

	def showsyntaxerror(self, *args, **kwargs):
		_, error_val, _ = sys.exc_info()
		self.error = error_val

	def reset(self):
		self.error = None
		self.resetbuffer()


@profile
def get_deletion_ranges(root):
	if not hasattr(root, "body"):
		return

	children = root.body
	if not children:
		return

	*rest_nodes, last_node = children

	with suppress(ValueError):
		begin_lineno = min(chain.from_iterable(ast_get_begin_linenos(node) for node in rest_nodes))
		end_lineno   = max(chain.from_iterable(ast_get_end_linenos(node)   for node in rest_nodes))
		yield begin_lineno, end_lineno

	yield from get_deletion_ranges(last_node)


@profile
def ast_get_begin_linenos(root):
	return [node.lineno - 1 for node in ast.walk(root) if hasattr(node, 'lineno')]


@profile
def ast_get_end_linenos(root):
	return [node.end_lineno for node in ast.walk(root) if hasattr(node, 'end_lineno')]


def is_functional(raw_line):
	line = f"{raw_line}\n "
	return is_influential(line)


def is_influential(line):
	if is_empty(line):
		return False

	with suppress(Exception):
		tree = ast.parse(line)
		nodes = ast.iter_child_nodes(tree)
		return bool(list(nodes))

	return True


def is_empty(line):
	return not line.strip()
