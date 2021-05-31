from itertools import zip_longest
import re

from .console import DryRunConsole, is_functional, is_empty, is_influential


def profile(func):
	return func


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

		# if self._parse_error_space_nonempty_line(line, console_space):
		# 	return True

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
		self.add_lines(console_nospace, split=False)
		return True

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
		self.queue_lines()  # no split
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

	body = block[:len(block) - len(padding)]
	assert body + padding == block
	return body, padding


@profile
def get_code_blocks(code):
	parser = Parser()
	blocks = parser.parse(code)
	assert "".join(blocks) == code
	return blocks
