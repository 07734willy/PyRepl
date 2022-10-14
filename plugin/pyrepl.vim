fun! s:IsWindows() abort
	return has("win32") || has("win64")
		\ || has("win16") || has("win95")
		\ || has("win32unix")  " Cygwin
		\ || has("gui_win32") || has("gui_win32s")
endfun

if !exists("g:pyrepl_timeout")
	let g:pyrepl_timeout = 1
endif

if !exists("g:pyrepl_logfile")
	let g:pyrepl_logfile = ""
endif

if !exists("g:pyrepl_debug")
	let g:pyrepl_debug = 0
endif

if !exists("g:pyrepl_interpreter")
	if executable("python") && s:IsWindows()  " prefer python > python3 on Win
		let g:pyrepl_interpreter = "python"
	elseif executable("python3")              " prefer python3 > python on Unix
		let g:pyrepl_interpreter = "python3"
	elseif executable("python")
		let g:pyrepl_interpreter = "python"
	elseif executable("py")
		let g:pyrepl_interpreter = "py"
	endif
endif

fun! s:AppendPythonPath(path) abort
	let l:sep = s:IsWindows() ? ";" : ":"
	let l:realpath = resolve(a:path)

	if has("win32unix")
		" In cygwin / git bash, filepaths are Unix, but PYTHONPATH may need to be
		" WIN format (particularly if there's already paths present)
		let l:drive_pattern = '^/\([a-zA-Z]\)/'
		" try to do a quick regex sub, as opposed to firing up another proc
		" ontop of python (this is windows afterall)
		if l:realpath =~ l:drive_pattern
			let l:fullpath = substitute(l:realpath, l:drive_pattern, '\1:/', "")
		elseif executable("cygpath")
			let l:fullpath = systemlist("cygpath --windows " . shellescape(l:realpath))[0]
		else
			echoerr "Unable to convert filepath from Unix->WIN without cygpath. Please create an issue ticket on github with details"
		endif
	else
		let l:fullpath = l:realpath
	endif

	if $PYTHONPATH == ""
		let $PYTHONPATH = l:fullpath
	else
		let $PYTHONPATH .= l:sep . l:fullpath
	endif
endfun

fun! s:Clamp(value, lower, upper) abort
	return max([a:lower, min([a:value, a:upper])])
endfun

fun! s:DelComments(start, stop, keywords) abort
	let [l:bufnum, l:lnum, l:col, l:off, l:curswant] = getcurpos()
	let l:mid = s:Clamp(l:lnum, a:start, a:stop)

	if l:mid < a:stop
		sil execute l:mid + 1 . "," . a:stop .  "g/^# \\%\\(" . a:keywords . "\\): /d"
	endif
	sil execute a:start . "," . l:mid . "g/^# \\%\\(" . a:keywords . "\\): /d|let l:lnum -= 1"

	call setpos(".", [bufnum, lnum, col, off, curswant])
endfun

fun! s:StripComments(start, stop, ...) abort
	let l:mode = get(a:, 1, 'output')

	if l:mode == "all"
		let l:regex = "in\\|out\\|info\\|error"
	elseif l:mode == "output"
		let l:regex = "out\\|info\\|error"
	elseif l:mode == "input"
		let l:regex = "in"
	elseif l:mode == "error"
		let l:regex = "error"
	else
		echoerr "Invalid Option: " . l:mode
	endif
	call s:DelComments(a:start, a:stop, l:regex)
endfun

fun! s:StripOptions(ArgLead, CmdLine, CursorPos) abort
	return join(["all", "input", "output", "error"], "\n")
endfun

fun! s:EvalCode(start, stop) abort
	if !exists("g:pyrepl_interpreter")
		echohl ErrorMsg
		echomsg "PyRepl: No Interpreter"
		echohl None
		return
	endif
	let l:buffersize = line('$')
	call s:StripComments(a:start, a:stop, 'output')
	let l:true_stop = a:stop - (l:buffersize - line('$'))

	let l:old_pypath = $PYTHONPATH
	
	let l:source = join(getline(a:start, true_stop), "\n")
	let l:command = g:pyrepl_interpreter . " -m pyrepl -t " . g:pyrepl_timeout . " -o " . (a:start - 1)

	if g:pyrepl_logfile != ""
		let l:command .= " --log " . g:pyrepl_logfile
	endif

	if g:pyrepl_debug
		let l:command .= " --debug"
	endif

	try
		call s:AppendPythonPath(expand("%:p:h"))
		let l:output = system(command, source)
	finally
		let $PYTHONPATH = old_pypath
	endtry

	for [lineno, text] in json_decode(output)
		if lineno == -1
			echohl ErrorMsg
			echomsg text
			echohl None
			return
		endif
		call append(lineno, split(text, "\n", 1))
	endfor
endfun

call s:AppendPythonPath(expand("<sfile>:p:h:h") . '/src')

command -range=% -bar PyReplEval call s:EvalCode(<line1>, <line2>)
command -range=% -bar -nargs=? -complete=custom,s:StripOptions PyReplStrip call s:StripComments(<line1>, <line2>, <f-args>)
