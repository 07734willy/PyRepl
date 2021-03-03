
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

fun! s:DelComments(keyword) abort
	let l:source = join(getline(1,'$'), "\n")

	sil execute "%g/^# " . a:keyword . ": /d"
	if source =~ "\\%(^\\|\\n\\)# ". a:keyword . ": "
		call setpos(".", getpos("'`"))
	endif
endfun

fun! pyrepl#StripOutput() abort
	call s:DelComments("out")
endfun

fun! pyrepl#StripInput() abort
	call s:DelComments("in")
endfun

fun! pyrepl#StripAll() abort
	call pyrepl#StripInput()
	call pyrepl#StripOutput()
endfun

fun! pyrepl#EvalBuffer() abort
	call pyrepl#StripOutput()
	
	let l:source = join(getline(1,'$'), "\n")
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


