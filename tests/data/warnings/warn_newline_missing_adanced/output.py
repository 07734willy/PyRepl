

print("\n"*4, 'nonempty', end="")
# out: 
# out: 
# out: 
# out: 
# out:  nonempty
# warn: Missing trailing newline

print("foo")
# out: foo

print(*['aaa\n']*3, 'ccc', end="")
# out: aaa
# out:  aaa
# out:  aaa
# out:  ccc
# warn: Missing trailing newline

