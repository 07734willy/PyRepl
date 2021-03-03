from .helper import run_test


def test_stateful():
	run_test(
"""
x = 1
y = 2
print(x + y)
""", 
"""
x = 1
y = 2
print(x + y)
# out: 3
""")
