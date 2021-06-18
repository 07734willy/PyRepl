

class Line:
	def __init__(self, text):
		self.buffer_lines = [text]

	def extend(self, other):
		self.buffer_lines.extend(other.buffer_lines)

	@profile
	def text(self):
		return "\n".join(self.buffer_lines)



