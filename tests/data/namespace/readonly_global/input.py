

def print_val():
	print(glob_x)


glob_x = 2
print_val()


glob_y = 3

def mutate_val():
	global glob_y
	glob_y = 2

mutate_val()
glob_y
