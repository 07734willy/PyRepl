from contextlib import suppress
from pprint import pprint
import ast

from .console import DryRunConsole, is_functional, is_empty

def get_parse_error(code, mode):
	try:
		compile(code, "<file>", mode)
	except SyntaxError as error:
		return error

def get_parse_single_error(code):
	return get_parse_error(code, "single")

def get_parse_exec_error(code):
	return get_parse_error(code, "exec")

def parse_code(code):
	return compile(code, "<file>", "single", flags=ast.PyCF_ONLY_AST)

MULTILINE_EXCEPTION = get_parse_single_error("0\n0")

def compare_exception_types(e1, e2):
	return type(e1) == type(e2) and e1.msg == e2.msg

def compare_exceptions(e1, e2):
	return type(e1) == type(e2) and e1.args == e2.args

def get_true_error_lineno(code, error):
	error_lineno = error.lineno - 1
	code_lines = code.split("\n", error_lineno+1)

	offset = error.offset
	error_line = code_lines[error_lineno]

	while offset > len(error_line):
		offset -= len(error_line) + 1
		error_lineno -= 1
		error_line = code_lines[error_lineno]
	return error_lineno

def take_until_line(code, lineno):
	# *first_half_lines, _ = text.split("\n", lineno+1)
	first_half_lines = split_lines(code)[:lineno+1]
	first_half = "".join(first_half_lines)
	return first_half

def is_valid_segment_start(line):
	if not is_functional(line):
		return False

	console = DryRunConsole()
	console.push(line)
	return not console.error

import re

def split_lines(code):
	lines = re.findall(r".+\n?|.*\n", code)
	return lines

class Block:
	def __init__(self, code):
		code_lines = split_lines(code)

		top_pad_lines, code_lines    = self.split_padding(code_lines)
		bottom_pad_lines, code_lines = self.split_padding(code_lines[::-1])
		
		self.top_pad    = "".join(top_pad_lines)
		self.bottom_pad = "".join(bottom_pad_lines[::-1])
		self.code       = "".join(code_lines[::-1])

	def split_padding(self, code_lines):
		for idx, line in enumerate(code_lines):
			if is_functional(line):
				padding_lines     = code_lines[:idx]
				code_subset_lines = code_lines[idx:]
				
				return padding_lines, code_subset_lines
		return code_lines, ""

	def shift_padding(self, other):
		other.bottom_pad += self.top_pad
		self.top_pad = ""

	@property
	def code_with_padding(self):
		return self.top_pad + self.code + self.bottom_pad

	@property
	def size(self):
		return len(self.code_with_padding)

	@property
	def padding(self):
		return self.bottom_pad

	@property
	def body(self):
		return self.top_pad + self.code

	def __repr__(self):
		return f"<Block: ({repr(self.top_pad)}, {repr(self.code)}, {repr(self.bottom_pad)})>"
		

def get_next_error_block_content(code, error):
	code_lines = split_lines(code)
	error_lineno = error.lineno - 1
	
	for lineno, line in enumerate(code_lines[error_lineno+1:], error_lineno+1):
		if is_valid_segment_start(line):
			return "".join(code_lines[:lineno])
	return code

def get_block_subset(code):
	code_lines = split_lines(code)
	ast_node = parse_code(code).body[0]
	# ast_node = ast.parse(code).body[0]
	end_lineno = ast_node.end_lineno - 1

	subset_lines = code_lines[:end_lineno+1]
	return "".join(subset_lines)

import sys

def get_next_block_content(code):
	if is_empty(code):
		return code

	error = get_parse_single_error(code)
	exec_error = get_parse_exec_error(code)

	if error is None:
		#print(" >> LAST LINE", file=sys.stderr)
		return get_block_subset(code)

	if compare_exceptions(error, exec_error):
		#print(" >> ERROR LINE", file=sys.stderr)
		return get_next_error_block_content(code, error)

	if compare_exception_types(error, MULTILINE_EXCEPTION):
		#print(" >> SIMPLE STATEMENT", file=sys.stderr)
		return take_until_line(code, error.lineno-1)

	#print(" >> COMPLEX STATEMENT", file=sys.stderr)
	error_lineno = get_true_error_lineno(code, error)
	return take_until_line(code, error_lineno-1)


def get_code_blocks(code):
	blocks = []

	while code:
		content = get_next_block_content(code)
		block = Block(content)
		code = code[block.size:]
		blocks.append(block)

	prev_block, *rest = blocks

	for curr_block in rest:
		curr_block.shift_padding(prev_block)
		prev_block = curr_block

	#print(blocks, file=sys.stderr)
	return blocks
	

def main():
	import sys
	code = sys.stdin.read()
	blocks = list(get_code_blocks(code))

	pprint(blocks)

	print("".join(block.code_with_padding for block in blocks))
	assert "".join(block.code_with_padding for block in blocks) == code

if __name__ == "__main__":
	main()
