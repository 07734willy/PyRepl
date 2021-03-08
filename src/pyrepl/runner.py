from threading import Thread
from json import dump
import sys

from .interpreter import Interpreter
from .fdio import IOBuffer

def write_result(output):
	dump(output, sys.stdout)

def build_error(msg):
	return [[-1, msg]]

def run_code(code, timeout, offset):
	code = "\n" * offset + code
	with IOBuffer() as (fdin, fdout):
		interpreter = Interpreter(fdin, fdout)
		thread = Thread(target=interpreter.eval, args=(code,))
		thread.daemon = True
		thread.start()
		thread.join(timeout)
	
	if thread.is_alive():
		return build_error("PyRepl: Timed out")
	return interpreter.output

