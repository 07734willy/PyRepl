syn match PyReplComment '^# \%(in\|out\|info\): .*' contains=PyReplIn,PyReplOut,PyReplInfo
syn match PyReplIn '# in:' contained
syn match PyReplOut '# out:' contained
syn match PyReplInfo '# info:' contained

fun! s:SetDefaultHighlight(name, value) abort
	if synIDattr(synIDtrans(hlID(a:name)), "fg") == ""
		execute "hi " . a:name . " ctermfg=" . a:value
	endif
endfun

fun! s:SetDefaultColors() abort
	call s:SetDefaultHighlight("PyReplIn", "green")
	call s:SetDefaultHighlight("PyReplOut", "darkgrey")
	call s:SetDefaultHighlight("PyReplInfo", "yellow")
	call s:SetDefaultHighlight("PyReplComment", "grey")
endfun

augroup PyReplColors
	autocmd!
	autocmd ColorScheme * call s:SetDefaultColors()
augroup END

call s:SetDefaultColors()

let $PYTHONPATH .= ":" . resolve(expand("<sfile>:p:h:h") . '/src')

if !exists("g:pyrepl_timeout")
	let g:pyrepl_timeout = 1
endif

if !exists("g:pyrepl_interpreter")
	if executable("python3")
		let g:pyrepl_interpreter = "python3"
	else
		let g:pyrepl_interpreter = "python"
	endif
endif

fun! s:Clamp(value, lower, upper) abort
	return max([a:lower, min([a:value, a:upper])])
endfun

fun! s:DelComments(start, stop, keywords) abort
	let [l:bufnum, l:lnum, l:col, l:off, l:curswant] = getcurpos()
	let l:mid = s:Clamp(l:lnum, a:start, a:stop)

	sil execute l:mid . "," . a:stop .  "g/^# \\%\\(" . a:keywords . "\\): /d"
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
	let l:buffersize = line('$')
	call s:StripComments(a:start, a:stop, 'output')
	let l:true_stop = a:stop - (l:buffersize - line('$'))
	
	let l:source = join(getline(a:start, true_stop), "\n")
	let l:command = g:pyrepl_interpreter . " -m pyrepl " . g:pyrepl_timeout
	let l:output = system(command, source)

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
