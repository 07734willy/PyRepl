
if !exists('g:pyrepl_set_colors')
	let g:pyrepl_set_colors = 1
endif
if !exists('g:pyrepl_map_keys')
	let g:pyrepl_map_keys = 1
endif


if g:pyrepl_map_keys
	nnoremap <buffer> <silent> <leader>ee :PyReplEval<CR>
	nnoremap <buffer> <silent> <leader>eu :0,PyReplEval<CR>
	vnoremap <buffer> <silent> <leader>e :'<,'>PyReplEval<CR>

	nnoremap <buffer> <silent> <leader>c :PyReplStrip output<CR>
	vnoremap <buffer> <silent> <leader>c :'<,'>PyReplStrip output<CR>
endif

syn match PyReplComment '^# \%(in\|out\|warn\): .*' contains=PyReplRest,PyReplIn,PyReplOut,PyReplWarn
syn match PyReplIn '# in:' contained
syn match PyReplOut '# out:' contained
syn match PyReplWarn '# warn:' contained

fun! s:GetHighlightColor(name, default) abort
	let l:colorval = synIDattr(synIDtrans(hlID(a:name)), "fg")
	return colorval == "" ? a:default : colorval
endfun

fun! s:SetDefaultHighlight(name, value) abort
	let l:colorval = s:GetHighlightColor(a:name, a:value)
	execute "hi " . a:name . " ctermfg=" . colorval
endfun

let s:color_pyrepl_in      = s:GetHighlightColor("PyReplIn", "green")
let s:color_pyrepl_out     = s:GetHighlightColor("PyReplOut", "darkgrey")
let s:color_pyrepl_info    = s:GetHighlightColor("PyReplInfo", "yellow")
let s:color_pyrepl_comment = s:GetHighlightColor("PyReplComment", "grey")

fun! s:SetDefaultColors() abort
	call s:SetDefaultHighlight("PyReplIn", s:color_pyrepl_in)
	call s:SetDefaultHighlight("PyReplOut", s:color_pyrepl_out)
	call s:SetDefaultHighlight("PyReplInfo", s:color_pyrepl_info)
	call s:SetDefaultHighlight("PyReplComment", s:color_pyrepl_comment)
endfun

augroup PyReplColors
	autocmd! * <buffer>
	autocmd ColorScheme <buffer> call s:SetDefaultColors()
augroup END

