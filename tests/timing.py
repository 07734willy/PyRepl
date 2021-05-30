import sys

from pyrepl.runner import run_code, write_result

DEFAULT_TIMEOUT = 1

def main():
	try:
		timeout = float(sys.argv[1])
	except:
		timeout = DEFAULT_TIMEOUT

	try:
		offset = int(sys.argv[2]) 
		assert offset >= 0
	except:
		offset = 0

	code = sys.stdin.read()
	result = run_code(code, timeout, offset)
	write_result(result)

if __name__ == "__main__":
	main()
