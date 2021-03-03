# Vim-PyRepl 
![example workflow](https://github.com/07734willy/Vim-PyRepl/actions/workflows/python-package.yml/badge.svg)

A vim plugin for executing python code within the buffer, displaying the results. A middle-ground between using a full-blown python notebook as with Jupyter or IPython, and merely using the Python REPL. This allows the user to write their code in their normal vim environment, run and see the result inline, and then make any corrections, all without leaving vim. 

### Installation

To install the plugin, you'll likely want to use some plugin manager. Below is an example using Vim-Plug, but you're free to use whichever you prefer.

#### [**Vim-Plug**](https://github.com/junegunn/vim-plug)

Once you've installed Vim-Plug, drop the following into your vimrc, reopen vim, then `:PlugInstall`.

```vim
call plug#begin('~/.vim/plugged')
Plug '07734willy/Vim-PyRepl'
call plug#end()
filetype plugin on
```

### Customization

There are a handful of variables you can set to tweak the plugin's behavior.

**Behavioral**
```vim
" Dictates how long (in seconds) to wait before killing the python process
" Note that since vim is single-threaded, it will hang until the python process terminates
let g:pyrepl_timeout = 1

" This can be changed to the path of the specific executable you wish to have run your code
" If you are using virtualenv, you should be fine. This is for others who don't use that
let g:pyrepl_interpreter = "python"
```

**Mappings**
```vim
" Note that the default mappings use the <leader> key
" By default, <leader> is bound to '\'. You can change this with `let mapleader = ...`
" You can also freely swap <leader> for something else in any of these mappings, or omit it entirely.

" Set this if you intend to set the mappings yourself
let g:pyrepl_map_keys = 0

" By default, buffer evaluation is mapped to <leader>r
nnoremap <buffer> <silent> <leader>r :call pyrepl#EvalBuffer()<CR>

" By default, clearing output is mapped to <leader>c
nnoremap <buffer> <silent> <leader>c :call pyrepl#StripOutput()<CR>

" There are two other methods you may wish to map:
" pyrepl#StripInput()
" pyrepl#StripAll()
```

**Aesthetics**
```vim
" Set this if you intend to set the colors yourself
let g:pyrepl_set_colors = 0

" Below are the default colors of the highlight groups, feel free to override them
hi PyReplIn ctermfg=green
hi PyReplOut ctermfg=darkgrey
hi PyReplWarn ctermfg=darkred
hi PyReplComment ctermfg=grey
```


