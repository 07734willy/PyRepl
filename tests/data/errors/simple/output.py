
x = 2

x =
# error:   File "<string>", line 4
# error:     x =
# error:        ^
# error: SyntaxError: invalid syntax

1 // 0
# error: Traceback (most recent call last):
# error:   File "<string>", line 10, in <module>
# error: ZeroDivisionError: integer division or modulo by zero

y = 2

raise ValueError("Foo")
# error: Traceback (most recent call last):
# error:   File "<string>", line 17, in <module>
# error: ValueError: Foo
