
x = 1

y = 
# error:   File "<string>", line 4
# error:     y =
# error:        ^
# error: SyntaxError: invalid syntax
x = 3
x
# out: 3

if x:
	x =
# error:   File "<string>", line 14
# error:     x =
# error:       ^
# error: SyntaxError: invalid syntax
x
# out: 3

y = 3
if y:
	y = 
elif y:
	y = 
# error:   File "<string>", line 24
# error:     y =
# error:        ^
# error: SyntaxError: invalid syntax
if y:
	y = 
# error:   File "<string>", line 32
# error:     y =
# error:        ^
# error: SyntaxError: invalid syntax
y
# out: 3

if y:
	y = 
	if y:
		a =
	b =
	c =
d =
# error:   File "<string>", line 41
# error:     y =
# error:        ^
# error: SyntaxError: invalid syntax

if x:
	x
'''
x
'''
# out: '\nx\n'
y =
x =
# error:   File "<string>", line 58
# error:     y =
# error:       ^
# error: SyntaxError: invalid syntax
'''
'''
# out: '\n'
x =
# error:   File "<string>", line 67
# error:     x =
# error:       ^
# error: SyntaxError: invalid syntax

