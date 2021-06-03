from pyrepl.segments import get_segments
import pytest

@pytest.mark.timeout(0.1)
def test_parsing_many_statements():
	statement = "x = 2"

	code = "\n".join([statement] * 1000)

	get_segments(code)

@pytest.mark.timeout(0.1)
def test_parsing_construct_statements():
	if_statement = "if True:"
	statements = ["\tx = 3"] * 1000

	code = if_statement + "\n" + "\n".join(statements)
	
	get_segments(code)

@pytest.mark.timeout(0.01)
def test_parsing_else_statements():
	begin_stmt = "if True:\n\tpass\nelse:"
	statements = ["\tx = 3"] * 1000

	code = begin_stmt + "\n" + "\n".join(statements)
	
	get_segments(code)

@pytest.mark.timeout(0.1)
def test_parsing_elif_ladder():
	begin_stmt = "if True:\n\tx = 4"
	middle_stmt = "elif False:\n\tx = 4"

	code = "\n".join([begin_stmt] + [middle_stmt] * 300)

	get_segments(code)


