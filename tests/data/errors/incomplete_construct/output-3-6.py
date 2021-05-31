
if True:
	pass
else:
	pass
elif False:
	pass
# error:   File "<string>", line 6
# error:     elif False:
# error:        ^
# error: SyntaxError: invalid syntax



try:
	pass
finally:
	pass
except:
	pass
# error:   File "<string>", line 19
# error:     except:
# error:          ^
# error: SyntaxError: invalid syntax

x = 1

except:
	pass
# error:   File "<string>", line 28
# error:     except:
# error:          ^
# error: SyntaxError: invalid syntax

x = 2

else:
	pass
# error:   File "<string>", line 37
# error:     else:
# error:        ^
# error: SyntaxError: invalid syntax


def decor(func):
	return func


@decor
x = 2
# error:   File "<string>", line 50
# error:     x = 2
# error:     ^
# error: SyntaxError: invalid syntax
