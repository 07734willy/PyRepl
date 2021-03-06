
x = 2

x = 
# out:   File "<string>", line 4
# out:     x = 
# out:         ^
# out: SyntaxError: invalid syntax

1 // 0
# out: Traceback (most recent call last):
# out:   File "<string>", line 10, in <module>
# out: ZeroDivisionError: integer division or modulo by zero

y = 2

raise ValueError("Foo")
# out: Traceback (most recent call last):
# out:   File "<string>", line 17, in <module>
# out: ValueError: Foo
