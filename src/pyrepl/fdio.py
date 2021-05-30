from io import StringIO
import sys

def clear_fd(fd):
	fd.truncate(0)
	fd.seek(0)

def write_fd(fd, data):
	fd.write(data)
	fd.seek(0)

def append_fd(fd, data):
	fd.write(data)

def read_fd(fd):
	return fd.getvalue()

class StdinIO(StringIO):
	def __init__(self, fdout):
		self.fdout = fdout
		super().__init__()

	def read(self, *args, **kwargs):
		result = super().read(*args, **kwargs)
		self.fdout.write(result)
		return result
	
	def readline(self, *args, **kwargs):
		result = super().readline(*args, **kwargs)
		self.fdout.write(result)
		return result
	
	def readlines(self, *args, **kwargs):
		result = super().readlines(*args, **kwargs)
		self.fdout.writelines(result)
		return result

class IOBuffer:
	debug = True
	def __init__(self):
		self.stdin  = sys.stdin
		self.stdout = sys.stdout
		self.stderr = sys.stderr

	def __enter__(self):
		sys.stdout = StringIO()
		if self.debug:
			stderr = StringIO()
		else:
			stderr = sys.stderr = StringIO()
		sys.stdin = StdinIO(sys.stdout)
		return sys.stdin, sys.stdout, stderr

	def __exit__(self, type_, value, traceback):
		sys.stdin  = self.stdin
		sys.stdout = self.stdout
		if not self.debug:
			sys.stderr = self.stderr
			return True

