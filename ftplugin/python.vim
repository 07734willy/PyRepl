
if !exists('g:pyrepl_mapkeys')
	let g:pyrepl_mapkeys = 1
endif

if g:pyrepl_mapkeys
	nnoremap <buffer> <silent> <localleader>ee :PyReplEval<CR>
	nnoremap <buffer> <silent> <localleader>eu :0,PyReplEval<CR>
	vnoremap <buffer> <silent> <localleader>e :'<,'>PyReplEval<CR>

	nnoremap <buffer> <silent> <localleader>c :PyReplStrip output<CR>
	vnoremap <buffer> <silent> <localleader>c :'<,'>PyReplStrip output<CR>
endif

syn match PyReplComment '^# \%(in\|out\|info\|error\): .*' contains=PyReplIn,PyReplOut,PyReplInfo,PyReplError
syn match PyReplIn '# in:' contained
syn match PyReplOut '# out:' contained
syn match PyReplInfo '# info:' contained
syn match PyReplError '# error:' contained

fun! s:GetHighlightColors(name, fgdefault, bgdefault) abort
	let l:synid = synIDtrans(hlID(a:name))
	let l:fgcolor = synIDattr(synid, "fg")
	let l:bgcolor = synIDattr(synid, "bg")

	let l:fgcolor = fgcolor == "" ? a:fgdefault : fgcolor
	let l:bgcolor = bgcolor == "" ? a:bgdefault : bgcolor
	return [fgcolor, bgcolor]
endfun

fun! s:SetDefaultHighlight(name, colorvals) abort
	let [l:fgcolor, l:bgcolor] = a:colorvals
	let [l:fgcolor, l:bgcolor] = s:GetHighlightColors(a:name, fgcolor, bgcolor)

	if fgcolor != ""
		execute "hi " . a:name . " ctermfg=" . fgcolor 
	endif
	if bgcolor != ""
		execute "hi " . a:name . " ctermbg=" . bgcolor 
	endif
endfun

let s:color_pyrepl_in      = s:GetHighlightColors("PyReplIn", "green", "")
let s:color_pyrepl_out     = s:GetHighlightColors("PyReplOut", "darkgrey", "")
let s:color_pyrepl_info    = s:GetHighlightColors("PyReplInfo", "yellow", "")
let s:color_pyrepl_error   = s:GetHighlightColors("PyReplError", "darkyellow", "")
let s:color_pyrepl_comment = s:GetHighlightColors("PyReplComment", "grey", "")

fun! s:SetDefaultColors() abort
	call s:SetDefaultHighlight("PyReplIn", s:color_pyrepl_in)
	call s:SetDefaultHighlight("PyReplOut", s:color_pyrepl_out)
	call s:SetDefaultHighlight("PyReplInfo", s:color_pyrepl_info)
	call s:SetDefaultHighlight("PyReplError", s:color_pyrepl_error)
	call s:SetDefaultHighlight("PyReplComment", s:color_pyrepl_comment)
endfun

augroup PyReplColors
	autocmd! * <buffer>
	autocmd ColorScheme <buffer> call s:SetDefaultColors()
augroup END

call s:SetDefaultColors()
