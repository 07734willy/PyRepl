from code import InteractiveConsole
from itertools import cycle, zip_longest
import sys
import ast
import re

class DryRunConsole(InteractiveConsole):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.error = None

	def runcode(self, *args, **kwargs):
		pass

	def showsyntaxerror(self, *args, **kwargs):
		_, error_val, _ = sys.exc_info()
		self.error = error_val

	def reset(self):
		self.error = None
		self.resetbuffer()

	def push_source(self, source):
		lines = source.split("\n")
		for line in lines:
			self.push(line)

def is_functional(raw_line):
	line = f"{raw_line}\n "
	return is_influential(line)

def is_influential(line):
	try:
		tree = ast.parse(line)
		nodes = ast.iter_child_nodes(tree)
		return bool(list(nodes))
	except:
		return True

def is_empty(line):
	match = re.match(r"^\s*$", line)
	return bool(match)

class Parser:
	def __init__(self):
		self.console_queue = None
		self.interpreter_queue = None
		self.code_blocks = []

	def queue_lines(self):
		if self.console_queue is None:
			self.console_queue     = self.console_lines
			self.interpreter_queue = self.interpreter_lines
		else:
			self.console_queue     += f"\n{self.console_lines}"
			self.interpreter_queue += f"\n{self.interpreter_lines}"

	def add_lines(self):
		console = self.new_console()

		self.queue_lines()
		flush = not console.push(self.console_lines)
		#print(flush, repr(self.console_lines))

		if console.error:
			self.consume_error_lines(console)
		
		if flush:
			self.flush_lines()

	def flush_lines(self):
		if self.interpreter_queue is not None:
			self.code_blocks.append(self.interpreter_queue)
		self.console_queue = None
		self.interpreter_queue = None
	
	def new_console(self):
		console = DryRunConsole()
		if self.console_queue:
			console.push(self.console_queue)
		return console

	def pop_future_lines(self, line, lines):
		future_lines = [line]
		while lines and not is_functional(line):
			line = lines.pop()
			future_lines.append(line)
		return future_lines

	def fill_spaces(self, lines):
		return ["#" if is_empty(line) else line for line in lines]

	def _parse_nonempty_line(self, line):
		if not is_empty(line):
			#print(1)
			self.console_lines = line
			self.add_lines()
			return True
		return False

	def _parse_pending_space_line(self, line, console):
		pending_with_space = console.push(line)
		if pending_with_space:
			# NO SPLIT
			#print(2)
			self.console_lines = line
			self.add_lines()
			return True
		return False

	def set_future_lines(self, line):
		future_lines = self.pop_future_lines(line, self.lines)
		self.future_line = "\n".join(future_lines)

		future_lines_nospace = self.fill_spaces(future_lines)
		self.future_line_nospace = "\n".join(future_lines_nospace)

	def consume_error_lines(self, console):
		while self.lines:
			line = self.lines.pop()
			console.reset()

			self.interpreter_lines = line
			self.console_lines = line
		
			console.push(line)
			if is_functional(line) and not console.error:
				self.lines.append(line)
				break
			else:
				self.queue_lines()
		self.flush_lines()

	def _parse_nonempty_line(self, line):
		if is_empty(line):
			return False

		console0a = self.new_console()
		if self._parse_normal_nonempty_line(line, console0a):
			return True

		console0b = self.new_console()
		if self._parse_faked_empty_line(line, console0b):
			return True

		if self._parse_erroneous_nonempty_line(line):
			return True

		return False


	def _parse_normal_nonempty_line(self, line, console):
		console.push(line)
		if not console.error:
			#print(1.1)
			self.console_lines = line
			self.add_lines()
			return True
		return False

	def _parse_faked_empty_line(self, line, console):
		line = "\n" + line
		console.push_source(line)
		if not console.error:
			# SPLIT
			#print(1.2)
			self.flush_lines()
			self.console_lines = line
			self.add_lines()
			return True
		return False

	def _parse_erroneous_nonempty_line(self, line):
		self.console_lines = line
		self.add_lines()
		return True

	def _parse_pending_space_line(self, line, console):
		pending_with_space = console.push(line)
		if pending_with_space:
			# NO SPLIT
			#print(2)
			self.console_lines = line
			self.add_lines()
			return True
		return False

	def set_future_lines(self, line):
		future_lines = self.pop_future_lines(line, self.lines)
		self.future_line = "\n".join(future_lines)

		future_lines_nospace = self.fill_spaces(future_lines)
		self.future_line_nospace = "\n".join(future_lines_nospace)

	def consume_error_lines(self, console):
		while self.lines:
			line = self.lines.pop()
			console.reset()

			self.interpreter_lines = line
			self.console_lines = line
		
			console.push(line)
			if is_functional(line) and not console.error:
				self.lines.append(line)
				break
			else:
				self.queue_lines()
		self.flush_lines()

	def _parse_nospace_noerror_future_lines(self, console):
		console.push_source(self.future_line_nospace)
		if not console.error:
			# NO SPLIT
			#print(3)
			self.console_lines = self.future_line_nospace
			self.add_lines()
			return True
		return False
	
	def _parse_space_noerror_future_lines(self, console):
		console.push_source(self.future_line)
		if not console.error:
			# SPLIT
			#print(4)
			self.flush_lines()
			self.console_lines = self.future_line
			self.add_lines()
			return True
		return False

	def _parse_space_indenterror_future_lines(self, console):
		if isinstance(console.error, IndentationError):
			# NO SPLIT
			#print(5)
			self.console_lines = self.future_line_nospace
			self.add_lines()
			return True
		return False

	def _parse_space_othererror_future_lines(self):
		# SPLIT
		#print(6)
		self.flush_lines()
		self.console_lines = self.future_line
		self.add_lines()
		return True

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

		if self._parse_space_indenterror_future_lines(console3):
			return

		self._parse_space_othererror_future_lines()


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

def skew_block_padding(blocks):
	if not blocks:
		return blocks

	paddings, bodies = zip(*[get_block_prefix_padding(block) for block in blocks])
	new_pairs = zip_longest(bodies, paddings[1:], fillvalue="")

	new_blocks = ["".join(pair) for pair in new_pairs]
	new_blocks[0] = paddings[0] + new_blocks[0]
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

def get_code_blocks(code):
	parser = Parser()
	blocks = parser.parse(code)
	assert "\n".join(blocks) == code
	return blocks
	
