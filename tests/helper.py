from pyrepl import run_code

def inject_lines(source, lines):
	source_lines = source.split("\n")
	for lineno, text in lines:
		source_lines.insert(lineno, text.rstrip('\n'))
	return "\n".join(source_lines)

def run_test(source, expected):
	lines = run_code(source, 1)
	actual = inject_lines(source, lines)
	print(repr(actual), end="")
	assert actual == expected
	
