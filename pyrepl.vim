
let $PYTHONPATH .= ":" . expand("%:p:h")
let g:pyrepl_timeout = 1

fun! EvalBuffer() abort
	let source = join(getline(1,'$'), "\n")

	sil %g/^# out: /d
	if source =~ "\\%(^\\|\\n\\)# out: "
		call setpos(".", getpos("'`"))
	endif
	
	let source = join(getline(1,'$'), "\n")
	let output = system("python -m helper2 " . g:pyrepl_timeout, source)

	for [lineno, text] in json_decode(output)
		if lineno == -1
			echoerr text
		endif
		call append(lineno, split(text, "\n"))
	endfor
endfun


map <leader>r :call EvalBuffer()<CR>
