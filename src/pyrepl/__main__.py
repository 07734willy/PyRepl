import sys

from .runner import run_code, write_result

DEFAULT_TIMEOUT = 1

def main():
	try:
		timeout = float(sys.argv[1])
	except:
		timeout = DEFAULT_TIMEOUT

	code = sys.stdin.read()
	result = run_code(code, timeout)
	write_result(result)

if __name__ == "__main__":
	main()
