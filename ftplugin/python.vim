
if !exists('g:pyrepl_map_keys')
	let g:pyrepl_map_keys = 1
endif

if g:pyrepl_map_keys
	nnoremap <buffer> <silent> <leader>r :call pyrepl#EvalBuffer()<CR>
	nnoremap <buffer> <silent> <leader>c :call pyrepl#StripOutput()<CR>
endif

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
