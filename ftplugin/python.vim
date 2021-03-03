
if !exists('g:pyrepl_set_colors')
	let g:pyrepl_set_colors = 1
endif
if !exists('g:pyrepl_map_keys')
	let g:pyrepl_map_keys = 1
endif


if g:pyrepl_map_keys
	nnoremap <buffer> <silent> <leader>r :call pyrepl#EvalBuffer()<CR>
	nnoremap <buffer> <silent> <leader>c :call pyrepl#StripOutput()<CR>
endif

syn match PyReplComment '# \%(in\|out\|warn\): .*' contains=PyReplRest,PyReplIn,PyReplOut,PyReplWarn
syn match PyReplIn '# in:' contained
syn match PyReplOut '# out:' contained
syn match PyReplWarn '# warn:' contained

if g:pyrepl_set_colors
	hi PyReplIn ctermfg=green
	hi PyReplOut ctermfg=darkgrey
	hi PyReplWarn ctermfg=darkred
	hi PyReplComment ctermfg=grey
endif


