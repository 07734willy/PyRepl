import os
import pytest

from pyrepl import run_code

def inject_lines(source, lines):
	source_lines = source.split("\n")
	for offset, text in lines:
		for lineno, line in enumerate(text.split("\n"), offset):
			source_lines.insert(lineno, line)
	return "\n".join(source_lines)

def get_test_name(basepath, dirpath, filename):
	assert filename.endswith(".py")
	filename, _ = filename.rsplit(".", 1)

	assert filename == "input" or filename == "output"

	relpath = os.path.relpath(dirpath, basepath)
	return relpath.replace(os.path.sep, "_")

def read_file(path, kind):
	data_path = os.path.join(path, f"{kind}.py")
	with open(data_path, "r") as f:
		return f.read()

def load_parameterized(func):
	dirpath = os.path.dirname(os.path.abspath(__file__))
	path = os.path.join(dirpath, 'data')

	test_names = set()
	test_cases = []

	for root, dirs, files in os.walk(path):
		for filename in files:
			test_name = get_test_name(path, root, filename)
			if test_name in test_names:
				continue

			input_data  = read_file(root, "input")
			output_data = read_file(root, "output")
			test_names.add(test_name)
			test_cases.append((test_name, input_data, output_data))

	return pytest.mark.parametrize('test_name,source,expected', test_cases)(func)

@load_parameterized
def test_data(test_name, source, expected):
	lines = run_code(source, 1)
	actual = inject_lines(source, lines)
	assert actual == expected
