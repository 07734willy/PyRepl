
let $PYTHONPATH .= ":" . expand("<sfile>:p:h")
let g:pyrepl_timeout = 1

fun! DelComments(keyword) abort
	let source = join(getline(1,'$'), "\n")

	sil execute "%g/^# " . a:keyword . ": /d"
	if source =~ "\\%(^\\|\\n\\)# ". a:keyword . ": "
		call setpos(".", getpos("'`"))
	endif
endfun

fun! StripReplOutput() abort
	call DelComments("out")
endfun

fun! StripReplInput() abort
	call DelComments("in")
endfun

fun! StripReplAll() abort
	call StripReplInput()
	call StripReplOutput()
endfun

fun! EvalBuffer() abort
	call StripReplOutput()
	
	let source = join(getline(1,'$'), "\n")
	let output = system("python3 -m pyrepl " . g:pyrepl_timeout, source)

	for [lineno, text] in json_decode(output)
		if lineno == -1
			echohl ErrorMsg
			echomsg text
			echohl None
			return
		endif
		call append(lineno, split(text, "\n"))
	endfor
endfun


syn match PyReplComment '# \%(in\|out\): .*' contains=PyReplRest,PyReplIn,PyReplOut
syn match PyReplIn '# in:' contained
syn match PyReplOut '# out:' contained

