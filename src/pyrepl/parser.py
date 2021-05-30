from traceback import format_exception
import sys
import re

from .codeblock import get_code_blocks, get_block_postfix_padding

DOT = r"(?:(?<!\\)(?:\\\\)*\\\n|.)"
SOURCE_LINE = rf"(?:{DOT}*\n)"
INPUT_LINE  = rf"(?:# in: {DOT}*\n)"
EMPTY_LINE  = rf"(?:\n|#(?! in: ){DOT}*\n)"

SOURCES    = rf"(?:{EMPTY_LINE}|{INPUT_LINE}|{SOURCE_LINE})"
EXT_DATA   = rf"(?:{EMPTY_LINE}|{INPUT_LINE})"
EMPTY      = rf"(?:{EMPTY_LINE})"

class Segment:
	def __init__(self, entirety, data, code):
		self.entirety = entirety
		self.data = data
		self.code = code

		self.code_obj = None
		self._error = None

	@property
	def error(self):
		if self.code_obj is None and self._error is None:
			try:
				self.code_obj = compile(self.code, "<string>", "exec")
			except SyntaxError as e:
				self._error = "".join(format_exception(type(e), e, e.__traceback__))
		return self._error

	def get_syntax_error(self):
		try:
			compile(self.code, "<string>", "exec")
		except SyntaxError as e:
			return "".join(format_exception(type(e), e, e.__traceback__))

	def parse_input(self):
		regex = r"(?<!.)# in: (.*\n)"
		matches = re.finditer(regex, self.data)
		
		data = "".join(match.group(1) for match in matches)
		return data

	def __add__(self, other):
		return Segment(
			self.entirety + other.entirety,
			self.entirety + other.data,
			self.entirety + other.code,
		)

	@property
	def size(self):
		return len(self.entirety)

	@property
	def offset(self):
		return self.data.count("\n")

	@property
	def numlines(self):
		return self.entirety.count("\n")


def get_next_segment(code):
	regex = rf"^((({EMPTY}*{SOURCES}+?){EXT_DATA}*?){EMPTY}*)(?=[^\s#]|$)"
	return Segment(*re.match(regex, code).groups())

def get_segments_old(code):
	segments = []
	while code:
		segment = get_next_segment(code)
		segments.append(segment)
		code = code[segment.size:]
	del segment

	idx = 0
	while idx < len(segments):
		curr_segment = segments[idx]
		if not curr_segment.error:
			idx += 1
			continue

		if idx + 1 < len(segments):
			next_segment = segments[idx+1]
			new_segment = curr_segment + next_segment
			if new_segment.error != curr_segment.error:
				segments[idx] = new_segment
				del segments[idx+1]
				continue

		if idx - 1 >= 0:
			prev_segment = segments[idx-1]
			new_segment = prev_segment + curr_segment
			if new_segment.error != curr_segment.error:
				segments[idx-1] = new_segment
				del segments[idx]
				continue

		idx += 1
	return segments

def get_segments_new(code):
	blocks = get_code_blocks(code)
	
	segments = []
	for block in blocks:
		body, padding = get_block_postfix_padding(block)
		match = re.match(r"[\s\S]*(?<!.)# in: (?:.*\n)", padding)
		
		data = body
		if match:
			data += match.group(0)

		segment = Segment(block, data, body)
		segments.append(segment)

	return segments

USE_OLD_SEGMENTATION = False

def get_segments(code):
	if USE_OLD_SEGMENTATION:
		segments = get_segments_old(code)
	else:
		segments = get_segments_new(code)

	return segments

