from pyrepl.segments import get_segments
import pytest

REPEATS = 1000

@pytest.mark.timeout(0.1)
def test_parsing_many_statements():
	statement = "x = 2"
	repeats = REPEATS // 5

	code = "\n".join([statement] * repeats)

	segments = get_segments(code)
	assert len(segments) == repeats


@pytest.mark.timeout(0.1)
def test_parsing_many_unique_statements():
	statement = "x = {}"
	repeats = REPEATS // 5

	code = "\n".join(statement.format(i) for i in range(repeats))

	segments = get_segments(code)
	assert len(segments) == repeats


@pytest.mark.timeout(0.1)
def test_parsing_construct_statements():
	if_statement = "if True:"
	statements = ["\tx = 3"] * REPEATS

	code = if_statement + "\n" + "\n".join(statements)

	segments = get_segments(code)
	assert len(segments) == 1


@pytest.mark.timeout(0.1)
def test_parsing_else_statements():
	begin_stmt = "if True:\n\tpass\nelse:"
	statements = ["\tx = 3"] * REPEATS

	code = begin_stmt + "\n" + "\n".join(statements)

	segments = get_segments(code)
	assert len(segments) == 1


@pytest.mark.timeout(0.1)
def test_parsing_elif_ladder():
	begin_stmt = "if True:\n\tx = 4"
	middle_stmt = "elif False:\n\tx = 4"

	code = "\n".join([begin_stmt] + [middle_stmt] * (REPEATS // 3))

	segments = get_segments(code)
	assert len(segments) == 1


@pytest.mark.timeout(0.1)
def test_long_trailing_multiline_string():
	begin_stmt = "if True:\n\tx = 4"
	middle_stmt = "'''" + "\n" * REPEATS + "'''"
	end_stmt = "x = 5"

	code = "\n".join([begin_stmt] + [middle_stmt] + [end_stmt])

	segments = get_segments(code)
	assert len(segments) == 3


@pytest.mark.timeout(0.1)
def test_long_list():
	begin_stmt = "y = ["
	middle_stmt = "2,"
	end_stmt = "]"

	code = "\n".join([begin_stmt] + [middle_stmt] * REPEATS + [end_stmt])

	segments = get_segments(code)
	assert len(segments) == 1


@pytest.mark.timeout(0.1)
def test_many_backslash_lines():
	begin_stmt = "if True:\n\tx = 4\ny = \\"
	middle_stmt = "3 + \\"
	end_stmt = "2\nx = 5"

	code = "\n".join([begin_stmt] + [middle_stmt] * REPEATS + [end_stmt])

	segments = get_segments(code)
	assert len(segments) == 3


@pytest.mark.timeout(0.1)
def test_multiline_parenthesized_expression():
	begin_stmt = "if True:\n\tx = 4\n("
	middle_stmt = "3 and "
	end_stmt = "2)\nx = 5"

	code = "\n".join([begin_stmt] + [middle_stmt] * REPEATS + [end_stmt])

	segments = get_segments(code)
	assert len(segments) == 3
