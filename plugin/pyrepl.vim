let $PYTHONPATH .= ":" . resolve(expand("<sfile>:p:h:h") . '/src')

if !exists("g:pyrepl_timeout")
	let g:pyrepl_timeout = 1
endif

if !exists("g:pyrepl_interpreter")
	if executable("python3")
		let g:pyrepl_interpreter = "python3"
	elseif executable("python")
		let g:pyrepl_interpreter = "python"
	elseif executable("py")
		let g:pyrepl_interpreter = "py"
	endif
endif

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
		let l:regex = "in\\|out\\|info"
	elseif l:mode == "output"
		let l:regex = "out\\|info"
	elseif l:mode == "input"
		let l:regex = "in"
	else
		echoerr "Invalid Option: " . l:mode
	endif
	call s:DelComments(a:start, a:stop, l:regex)
endfun

fun! s:StripOptions(ArgLead, CmdLine, CursorPos) abort
	return join(["all", "input", "output"], "\n")
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
	let l:command = g:pyrepl_interpreter . " -m pyrepl " . g:pyrepl_timeout . " " . (a:start - 1)

	try
		let $PYTHONPATH .= ":" . resolve(expand("%:p:h"))
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

command -range=% -bar PyReplEval call s:EvalCode(<line1>, <line2>)
command -range=% -bar -nargs=? -complete=custom,s:StripOptions PyReplStrip call s:StripComments(<line1>, <line2>, <f-args>)
