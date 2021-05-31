from code import InteractiveConsole
from codeop import CommandCompiler
from contextlib import suppress
from itertools import cycle, zip_longest, chain
from copy import copy, deepcopy
import sys
import ast
import re

if 'profile' not in globals():
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
		# self.compile.compiler = Compile(self.compile.compiler) 
	
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
		if self.buffer:
			combined_lines = line + "\n" + self.buffer[-1]
			if not is_influential(combined_lines):
				return True

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
	return [node.lineno-1 for node in ast.walk(root) if hasattr(node, 'lineno')]

@profile
def ast_get_end_linenos(root):
	return [node.end_lineno for node in ast.walk(root) if hasattr(node, 'end_lineno')]
	

def is_functional(raw_line):
	line = f"{raw_line}\n "
	return is_influential(line)

def is_influential(line):
	if is_empty(line):
		return False
	try:
		tree = ast.parse(line)
		nodes = ast.iter_child_nodes(tree)
		return bool(list(nodes))
	except:
		return True

def is_empty(line):
	return not line.strip()

class Parser:
	def __init__(self):
		self.interpreter_queue = []
		self.code_blocks = []
		self.core_console = DryRunConsole()

	@profile
	def queue_lines(self, console_swap=None):
		self.interpreter_queue.append(self.interpreter_line)

		if console_swap:
			self.core_console = console_swap
		return bool(self.core_console.buffer)
		
	@profile
	def add_lines(self, console_swap, *, split):
		if split:
			self.flush_lines()

		flush = not self.queue_lines(console_swap)

		if self.core_console.error:
			self.consume_error_lines()
		
		if flush:
			self.flush_lines()

	@profile
	def flush_lines(self):
		if self.interpreter_queue:
			block = "\n".join(self.interpreter_queue)
			self.code_blocks.append(block)

		self.core_console.reset()
		self.interpreter_queue = []
	
	@profile
	def new_console(self):
		console = self.core_console.clone()
		return console

	@profile
	def consume_error_lines(self):
		while self.lines:
			line = self.lines.pop()
			self.core_console.reset()

			self.interpreter_line = line
		
			self.core_console.push(line)
			if is_functional(line) and not self.core_console.error:
				self.lines.append(line)
				break
			else:
				self.queue_lines()
		self.core_console.reset()
		self.flush_lines()

	@profile
	def _parse_nonempty_line(self, line):
		console_nospace = self.new_console()
		if self._parse_normal_nonempty_line(line, console_nospace):
			return True

		console_space = self.new_console()
		if self._parse_faked_empty_line(line, console_space):
			return True

		if self._parse_error_nospace_nonempty_line(line, console_space, console_nospace):
			return True
		
		#if self._parse_error_space_nonempty_line(line, console_space):
		#	return True

		return False

	@profile
	def _parse_normal_nonempty_line(self, line, console):
		console.push(line)
		if not console.error:
			self.add_lines(console, split=False)
			return True
		return False

	@profile
	def _parse_faked_empty_line(self, line, console):
		console.push("")
		console.push(line)
		if not console.error:
			self.add_lines(console, split=True)
			return True
		return False

	@profile
	def _parse_error_nospace_nonempty_line(self, line, console_space, console_nospace):
		#if isinstance(console_space.error, IndentationError):
		self.add_lines(console_nospace, split=False)
		return True
		#return False

	"""
	@profile
	def _parse_error_space_nonempty_line(self, line, console):
		self.add_lines(console, split=True)
		return True
	"""
	
	@profile
	def _parse_empty_line(self, line):
		if not is_empty(line):
			return False
		
		console = self.new_console()
		if self._parse_pending_space_line(line, console):
			return True

		if self._parse_nonpending_space_line(line):
			return True

		return False 

	@profile
	def _parse_pending_space_line(self, line, console):
		pending_with_space = console.push(line)
		if pending_with_space:
			self.add_lines(console, split=False)
			return True
		return False

	@profile
	def _parse_nonpending_space_line(self, line):
		self.queue_lines() # no split
		return True

	@profile
	def _parse_lines(self, line):
		self.interpreter_line = line
	
		if is_empty(line):
			return self._parse_empty_line(line)
		else:
			return self._parse_nonempty_line(line)

	@profile
	def parse(self, code):
		self.lines = code.split("\n")[::-1]

		while self.lines:
			line = self.lines.pop()
			self._parse_lines(line)

		self.flush_lines()

		skewed_blocks = skew_block_padding(self.code_blocks)
		return skewed_blocks

def merge_noninfluencial_blocks(blocks):
	output = blocks[:1]

	for block in blocks[1:]:
		if not is_influential(block):
			output.append(output.pop() + block)
		else:
			output.append(block)
	return output


def skew_block_padding(raw_blocks):
	if not raw_blocks:
		return raw_blocks
	
	blocks = [b + '\n' for b in raw_blocks[:-1]] + raw_blocks[-1:]
	blocks = merge_noninfluencial_blocks(blocks)

	paddings, bodies = zip(*[get_block_prefix_padding(block) for block in blocks])
	new_pairs = zip_longest(bodies, paddings[1:], fillvalue="")

	new_blocks = ["".join(pair) for pair in new_pairs]
	new_blocks[0] = paddings[0] + new_blocks[0]
	assert "\n".join(raw_blocks) == "".join(new_blocks)
	return new_blocks

def get_block_prefix_padding(block):
	lines = re.findall(r".+\n?|.*\n", block)
	
	padding = ""
	for line in lines:
		new_padding = padding + line
		if is_influential(new_padding):
			break
		padding = new_padding
	
	body = block[len(padding):]
	assert padding + body == block
	return padding, body

def get_block_postfix_padding(block):
	lines = re.findall(r".+\n?|.*\n", block)[::-1]

	padding = ""
	for line in lines:
		new_padding = line + padding
		if is_influential(new_padding):
			break
		padding = new_padding
	
	body = block[:len(block)-len(padding)]
	assert body + padding == block
	return body, padding

@profile
def get_code_blocks(code):
	parser = Parser()
	blocks = parser.parse(code)
	assert "".join(blocks) == code
	return blocks
	
