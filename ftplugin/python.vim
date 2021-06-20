
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
