from code import InteractiveConsole
from itertools import cycle, zip_longest
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
		self.error = None
		# self.compile.compiler = Compile(self.compile.compiler) 

	@profile
	def runcode(self, *args, **kwargs):
		pass

	@profile
	def showsyntaxerror(self, *args, **kwargs):
		_, error_val, _ = sys.exc_info()
		self.error = error_val

	@profile
	def reset(self):
		self.error = None
		self.resetbuffer()

	@profile
	def push_source(self, source):
		lines = source.split("\n")
		for line in lines:
			self.push(line)

@profile
def is_functional(raw_line):
	line = f"{raw_line}\n "
	return is_influential(line)

@profile
def is_influential(line):
	try:
		tree = ast.parse(line)
		nodes = ast.iter_child_nodes(tree)
		return bool(list(nodes))
	except:
		return True

@profile
def is_empty(line):
	match = re.match(r"^\s*$", line)
	return bool(match)

class Parser:
	def __init__(self):
		self.console_queue = None
		self.interpreter_queue = None
		self.code_blocks = []
		self.core_console = DryRunConsole()

	@profile
	def queue_lines(self, console_swap=None):
		if self.console_queue is None:
			self.console_queue	 = self.console_lines
			self.interpreter_queue = self.interpreter_lines
		else:
			self.console_queue	 += f"\n{self.console_lines}"
			self.interpreter_queue += f"\n{self.interpreter_lines}"

		if console_swap:
			self.core_console = console_swap
			return bool(self.core_console.buffer)
		else:
			return self.core_console.push(self.console_lines)

	@profile
	def add_lines(self, console_swap=None):
		flush = not self.queue_lines(console_swap)

		if self.core_console.error:
			self.consume_error_lines()
		
		if flush:
			self.flush_lines()

	@profile
	def flush_lines(self):
		if self.interpreter_queue is not None:
			self.code_blocks.append(self.interpreter_queue)
		self.core_console.reset()
		self.console_queue = None
		self.interpreter_queue = None
	
	@profile
	def new_console(self):
		# console = deepcopy(self.core_console)
		console = DryRunConsole()
		console.buffer = list(self.core_console.buffer)
		return console

	@profile
	def pop_future_lines(self, line, lines):
		future_lines = [line]
		while lines and not is_functional(line):
			line = lines.pop()
			future_lines.append(line)
		return future_lines

	@profile
	def fill_spaces(self, lines):
		return ["#" if is_empty(line) else line for line in lines]

	@profile
	def _parse_nonempty_line(self, line):
		if is_empty(line):
			return False

		console0a = self.new_console()
		if self._parse_normal_nonempty_line(line, console0a):
			return True

		console0b = self.new_console()
		if self._parse_faked_empty_line(line, console0b):
			return True

		if self._parse_erroneous_nonempty_line(line, console0a):
			return True

		return False

	@profile
	def _parse_normal_nonempty_line(self, line, console):
		console.push(line)
		if not console.error:
			#print(1.1)
			self.console_lines = line
			self.add_lines(console_swap=console)
			return True
		return False

	@profile
	def _parse_faked_empty_line(self, line, console):
		line = "\n" + line
		console.push_source(line)
		if not console.error:
			# SPLIT
			#print(1.2)
			self.flush_lines()
			self.console_lines = line
			self.add_lines(console_swap=console)
			return True
		return False

	@profile
	def _parse_erroneous_nonempty_line(self, line, console):
		# NO SPLIT
		self.console_lines = line
		self.add_lines(console_swap=console)
		return True

	@profile
	def _parse_pending_space_line(self, line, console):
		pending_with_space = console.push(line)
		if pending_with_space:
			# NO SPLIT
			#print(2)
			self.console_lines = line
			self.add_lines(console_swap=console)
			return True
		return False

	@profile
	def set_future_lines(self, line):
		future_lines = self.pop_future_lines(line, self.lines)
		self.future_line = "\n".join(future_lines)

		future_lines_nospace = self.fill_spaces(future_lines)
		self.future_line_nospace = "\n".join(future_lines_nospace)

	@profile
	def consume_error_lines(self):
		while self.lines:
			line = self.lines.pop()
			self.core_console.reset()

			self.interpreter_lines = line
			self.console_lines = line
		
			self.core_console.push(line)
			if is_functional(line) and not self.core_console.error:
				self.lines.append(line)
				break
			else:
				self.queue_lines()
		self.core_console.reset()
		self.flush_lines()

	@profile
	def _parse_nospace_noerror_future_lines(self, console):
		console.push(self.future_line_nospace)
		if not console.error:
			# NO SPLIT
			#print(3)
			self.console_lines = self.future_line_nospace
			self.add_lines(console_swap=console)
			return True
		return False
	
	@profile
	def _parse_space_noerror_future_lines(self, console):
		# TODO double check push_source -> push  replacement for correctness
		first_line, *rest_lines = self.future_line.split("\n")

		console.push(first_line)
		if rest_lines:
			console.push("\n".join(rest_lines))

		# console.push_source(self.future_line)
		if not console.error:
			# SPLIT
			#print(4)
			self.flush_lines()
			self.console_lines = self.future_line
			self.add_lines(console_swap=console)
			return True
		return False

	def _parse_space_indenterror_future_lines(self, console_space, console_nospace):
		if isinstance(console_space.error, IndentationError):
			# NO SPLIT
			#print(5)
			self.console_lines = self.future_line_nospace
			self.add_lines(console_swap=console_nospace)
			return True
		return False

	@profile
	def _parse_space_othererror_future_lines(self, console):
		# SPLIT
		#print(6)
		self.flush_lines()
		self.console_lines = self.future_line
		self.add_lines(console_swap=console)
		return True

	@profile
	def _parse_lines(self, line):
		self.interpreter_lines = line
		
		if self._parse_nonempty_line(line):
			return

		console1 = self.new_console()
		if self._parse_pending_space_line(line, console1):
			return
		
		self.set_future_lines(line)
		self.interpreter_lines = self.future_line

		console2 = self.new_console()
		if self._parse_nospace_noerror_future_lines(console2):
			return
		
		console3 = self.new_console()
		if self._parse_space_noerror_future_lines(console3):
			return

		if self._parse_space_indenterror_future_lines(console3, console2):
			return

		self._parse_space_othererror_future_lines(console3)


	@profile
	def parse(self, code):
		self.lines = code.split("\n")[::-1]

		while self.lines:
			self.console_lines = None
			self.interpreter_lines = None

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
	
