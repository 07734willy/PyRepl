from argparse import ArgumentParser
from pathlib import Path
from datetime import date
from traceback import format_exc
import logging
import sys
import os

from .runner import run_code, write_result, build_error

from logging import getLogger
logger = getLogger(__name__)


DEFAULT_TIMEOUT = 1
DEFAULT_LOG_FILE = Path(__file__).parents[2] / "logs" / f"debug.log"


def write_error(msg, parser):
	if not sys.stdout.isatty():
		write_result(build_error(f"PyRepl: {msg}"))
		return

	parser.print_help()
	print(f"Error: {msg}", file=sys.stderr)


def main():
	parser = ArgumentParser(description="Insert execution results as inline comments to stdin source")

	# Do NOT use type= in any of these- we don't want unformatted errors written to stderr
	parser.add_argument("-t", "--timeout", default=DEFAULT_TIMEOUT,
		help="Time to wait in seconds for Python to finish interpreting the *entire* source before forcibly exiting")
	parser.add_argument("-o", "--offset", default=0,
		help="Line number offset the interpreter by (to correct error message line numbers). Must be a nonnegative integer")
	parser.add_argument("--log", default=DEFAULT_LOG_FILE,
		help="Filepath of logfile (used for logging errors and debugging info)")
	parser.add_argument("--debug", action="store_true",
		help="Enables debug-mode logging (logs additional info besides explicit errors)")

	args = parser.parse_args()

	try:
		timeout = float(args.timeout)
	except ValueError:
		write_error("Invalid timeout set", parser)
		sys.exit(1)

	try:
		offset = int(args.offset)
		assert offset >= 0
	except (ValueError, AssertionError):
		write_error("Invalid line offset", parser)
		sys.exit(1)

	try:
		logpath = Path(args.log)
		if logpath == DEFAULT_LOG_FILE:  # logs/  might not exist
			os.makedirs(logpath.parent, exist_ok=True)
		assert logpath.parent.exists()
		assert not logpath.exists() or logpath.is_file()
	except AssertionError:
		write_error("Invalid logfile set", parser)
		sys.exit(1)

	# Actually start running

	loglevel = logging.DEBUG if args.debug else logging.ERROR
	logging.basicConfig(filename=logpath, level=loglevel,
		format="[%(asctime)s] [%(levelname)s] %(name)s::(%(funcName)s:%(lineno)s) - %(message)s")

	try:
		code = sys.stdin.read()
		result = run_code(code, timeout, offset)
		write_result(result)
	except Exception:
		logger.critical(format_exc())
		write_error("Interpreter crashed", parser)


if __name__ == "__main__":
	main()
