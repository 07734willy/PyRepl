import re

from .codeblock import get_code_blocks, get_block_postfix_padding

class Segment:
	def __init__(self, entirety, data, code):
		self.entirety = entirety
		self.data = data
		self.code = code

	def parse_input(self):
		regex = r"(?<!.)# in: (.*\n)"
		matches = re.finditer(regex, self.data)
		
		data = "".join(match.group(1) for match in matches)
		return data

	@property
	def size(self):
		return len(self.entirety)

	@property
	def offset(self):
		return self.data.count("\n")

	@property
	def numlines(self):
		return self.entirety.count("\n")

def get_segments(code):
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

