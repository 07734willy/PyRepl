
if True:
	pass
else:
	pass
elif False:
	pass
# out:   File "<string>", line 6
# out:     elif False:
# out:        ^
# out: SyntaxError: invalid syntax



try:
	pass
finally:
	pass
except:
	pass
# out:   File "<string>", line 19
# out:     except:
# out:          ^
# out: SyntaxError: invalid syntax

x = 1

except:
	pass
# out:   File "<string>", line 28
# out:     except:
# out:          ^
# out: SyntaxError: invalid syntax

x = 2

else:
	pass
# out:   File "<string>", line 37
# out:     else:
# out:        ^
# out: SyntaxError: invalid syntax


def decor(func):
	return func


@decor
x = 2
# out:   File "<string>", line 50
# out:     x = 2
# out:     ^
# out: SyntaxError: invalid syntax
