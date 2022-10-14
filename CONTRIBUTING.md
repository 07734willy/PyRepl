# Contributing

When contributing to this repository, please create an issue on Github before making any changes. There are a lot of things that *could* be added to PyRepl, but *should not*, because of the scope of the project.

## Vision


PyRepl is meant to be a lightweight Vim plugin to allow the user to see the effects of their Python code, right inside the buffer. It is meant to have aspects of both the Python REPL and of a full-blown Python Notebook like IPython or Jupyter, all within the editor. Such aspects include:

 - Displaying the value of an expression inline
 - Displaying errors at or near the block of code that creates them
 - Recovering from errors, and resuming execution on the next "good" block of code
 - Prompting for input near the relevant code block itself

Being a Vim plugin however, it is somewhat expected that the plugin implementation does not significantly restrict portability. For instance, if we ran a full-blown language server, that wouldn't be very lightweight, and it would strap on a modest number of dependencies to carry around with the plugin. Not to mention, running a language server would on some level violate the "spirit" of using Vim in the first place.

Another example of what could be considered beyond this project's scope would be caching code blocks. While it could provide some nice performance gains, it opens a whole crate of issues regarding dependencies between cells, deep copying python objects and dealing with weakrefs, etc. While this is useful, its pretty "heavy", and probably not well-suited for a Vim plugin, unless someone comes up with a drastic simplification.

We must keep these sorts of concepts in mind when considering new features and changes for PyRepl.

## Issues

Please create issues for any and all changes to be made. Whether that be bug reports, feature requests, code optimizations, etc. 

If submitting a bug report, please include:

 - A self-contained example of the Python code triggering the bug. Smaller / minified examples are appreciated.
 - The Vim / NeoVim version (`vim --version` / `nvim --version`)
 - The Python version triggering the issue (`python --version`, `python3 --version`, `py --version`)
 	- If you're not sure which of the above you're using, you can try using PyRepl in a new file containing only the text: `import sys; print(sys.version)`
 - The version of PyRepl you're experiencing the issue on (it may already be solved in a newer version, so check that too!)

## Environment

To setup your development environment, you need to first download and install the currently supported major versions of python [from python.org](https://www.python.org/downloads/). The supported versions are enumerated in the `tox.ini` file as well as in `.github/workflows/python-package.yml`.

### Testing

You can run the tests with the command `tox`. 

If you wish to test against one Python version at a time, I recommend setting up a virtual environment for a given Python version, and then installing the requirements. Afterwards, run

```bash
pip install --editable .[dev]
```

You'll then be able to run the tests with `pytest` as normal.

### Linting

You can run the linter with the command `flake8`.

## Pull Requests

If you have found an issue that you wish to tackle, you'll need to create a pull request to merge your contributions. Some notes when doing so:

 1. Do NOT break compatibility between Vim / NeoVim or system portability across Linux / Windows / Mac.
 	- There are no tests enforcing this, as it is extremely awkward to test vimscript
	- You generally won't break anything system-wise unless you're doing something really weird
	- You generally won't break anything Vim / NeoVim -wise from within Python
 2. All tests must pass.
 	- Performance tests must pass on Github Actions
 3. The linter (flake8) should exit cleanly
 4. Increment the version number in `setup.cfg` in line with [Semantic Versioning](https://semver.org/)
 5. If you are fixing a bug, you must add a regression test for said bug
 6. If you are adding a new feature, make sure it falls in line with the project **vision**, particularly if a maintainer has not yet commented on the issue
	

