from itertools import islice
import ast
import re

import sys

from .parser import Parser, compare_exception_types, is_empty

MULTILINE_EXCEPTION = Parser().get_parse_single_error("0\n0")


class Block:
	def __init__(self, parser, code):
		code_lines = split_lines(code)

		top_pad_lines, code_lines    = self.split_padding(parser, code_lines)
		bottom_pad_lines, code_lines = self.split_padding(parser, code_lines[::-1])

		self.top_pad    = "".join(top_pad_lines)
		self.bottom_pad = "".join(bottom_pad_lines[::-1])
		self.code       = "".join(code_lines[::-1])

	def split_padding(self, parser, code_lines):
		for idx, line in enumerate(code_lines):
			if parser.is_functional(line):
				padding_lines     = code_lines[:idx]
				code_subset_lines = code_lines[idx:]

				return padding_lines, code_subset_lines
		return code_lines, ""

	def shift_padding(self, other):
		other.bottom_pad += self.top_pad
		self.top_pad = ""

	@property
	def entirety(self):
		return self.top_pad + self.code + self.bottom_pad

	@property
	def size(self):
		return len(self.entirety)

	@property
	def padding(self):
		return self.bottom_pad

	@property
	def body(self):
		return self.top_pad + self.code

	def __repr__(self):
		return f"<Block: ({repr(self.top_pad)}, {repr(self.code)}, {repr(self.bottom_pad)})>"


def get_true_error_lineno(code, error):
	error_lineno = error.lineno - 1
	code_lines = code.split("\n", error_lineno + 1)

	if (3, 8) <= sys.version_info < (3, 9):
		offset = len(error.text) - 1
	else:
		offset = error.offset
	error_line = code_lines[error_lineno]

	while offset > len(error_line):
		offset -= len(error_line) + 1
		error_lineno -= 1
		error_line = code_lines[error_lineno]
	return error_lineno


def take_until_line(code, lineno):
	first_half_lines = split_lines(code, lineno + 1)
	first_half = "".join(first_half_lines)
	return first_half


def split_lines(code, count=None):
	matches = re.finditer(r".*\n?", code)
	lines = [m.group(0) for m in islice(matches, count)]
	return lines


def get_next_error_block_content(parser, code, error):
	code_lines = split_lines(code)
	error_lineno = error.lineno - 1

	for lineno, line in enumerate(code_lines[error_lineno + 1:], error_lineno + 1):
		if parser.is_valid_segment_start(line):
			return "".join(code_lines[:lineno])
	return code


def get_last_lineno(node):
	return max(e.end_lineno for e in ast.walk(node) if hasattr(e, "end_lineno"))


def get_block_subset(parser, code):
	code_lines = split_lines(code)
	module_body = parser.parse_code(code).body
	ast_node = module_body[0]

	try:
		end_lineno = get_last_lineno(ast_node) - 1
	except ValueError:
		assert len(module_body) == 1
		return code

	subset_lines = code_lines[:end_lineno + 1]
	return "".join(subset_lines)


def get_next_block_content(parser, code):
	if is_empty(code):
		return code

	error = parser.get_parse_single_error(code)
	if error is None:
		return get_block_subset(parser, code)

	if parser.compare_single_and_exec(code):
		return get_next_error_block_content(parser, code, error)

	if compare_exception_types(error, MULTILINE_EXCEPTION):
		return take_until_line(code, error.lineno - 1)

	error_lineno = get_true_error_lineno(code, error)
	return take_until_line(code, error_lineno - 1)


def get_code_blocks(code):
	parser = Parser()
	blocks = []

	while code:
		content = get_next_block_content(parser, code)
		parser.update_offset(content)
		block = Block(parser, content)

		code = code[block.size:]
		blocks.append(block)

	prev_block, *rest = blocks

	for curr_block in rest:
		curr_block.shift_padding(prev_block)
		prev_block = curr_block

	return blocks
