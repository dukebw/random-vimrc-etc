let mapleader = '-'

set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'

" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
Plugin 'tpope/vim-fugitive'
Plugin 'zeis/vim-kolor'
Plugin 'flazz/vim-colorschemes'
Plugin 'tpope/vim-commentary'
Plugin 'myusuf3/numbers.vim'
Plugin 'tpope/vim-surround'
Plugin 'tpope/vim-unimpaired'
Plugin 'tpope/vim-dispatch'
" NOTE(brendan): jedi-vim can sometimes get into a state where it lags a lot,
" apparently requiring system reboot to resolve
" Seems to go away with let g:jedi#show_call_signatures = "0"
" See this thread: https://github.com/davidhalter/jedi-vim/issues/217
Plugin 'davidhalter/jedi-vim'
Plugin 'dylon/vim-antlr'
Plugin 'yegappan/mru'
Plugin 'mbbill/undotree'
Plugin 'christoomey/vim-tmux-navigator'
Plugin 'tikhomirov/vim-glsl'
Plugin 'leafgarland/typescript-vim'
Plugin 'psf/black'
Plugin 'pangloss/vim-javascript'
Plugin 'mxw/vim-jsx'
Plugin 'dense-analysis/ale'
Plugin 'lervag/vimtex'
Plugin 'ervandew/supertab'

" plugin from http://vim-scripts.org/vim/scripts.html
" Plugin 'L9'
" " Git plugin not hosted on GitHub
" Plugin 'git://git.wincent.com/command-t.git'
" " git repos on your local machine (i.e. when working on your own plugin)
" Plugin 'file:///home/gmarik/path/to/plugin'
" " The sparkup vim script is in a subdirectory of this repo called vim.
" " Pass the path to set the runtimepath properly.
" Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" " Avoid a name conflict with L9
" Plugin 'user/L9', {'name': 'newL9'}

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
" filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line
"Personal settings
"More to be added soon
filetype plugin indent on
syntax on

colorscheme kolor

" No highlight after search on Ctrl+N
nmap <silent> <C-N> :silent noh<CR>

" Set tab stops to be 2 spaces
set tabstop=8
set softtabstop=8
set shiftwidth=8
set expandtab
" set smarttab

" Get rid of "O" delay
" set noesckeys

" Automatically load skeleton.
" au BufNewFile *.cpp 0r C:\work\cpp_header.txt | let IndentStyle = "cpp"

map ` :w<CR>
set guifont=Inconsolata:h11:cANSI

set autoindent

" Fold on syntax
:set foldmethod=syntax

" Autocomplete like BASH
set wildmode=longest,list

" matchit.vim
runtime macros/matchit.vim

"Note: This option must set it in .vimrc(_vimrc).  NOT IN .gvimrc(_gvimrc)!
" Disable AutoComplPop.
let g:acp_enableAtStartup = 0

set backupdir=$HOME/.vim/backupdir
set directory=$HOME/.vim/backupdir
set undodir=$HOME/.vim/undodir

set cscopequickfix=s-,c-,d-,i-,t-,e-

" noremap ,1 :make<CR>:cs reset<CR>
" noremap ,1 :!find . -iname "*.cshtml" > cscope.files && cscope -b -q -k<CR>:cs reset<CR>
noremap ,1 :!cscope -b -q -k<CR>:cs reset<CR>
noremap ,2 :cp<CR>
noremap ,3 :cn<CR>
noremap ,4 :cs reset<CR>

set cino+=(0

" autocommands
augroup syntax_generic
        autocmd!
        autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o
        autocmd FileType latex set sts=0 ts=0 sw=0
        autocmd FileType css setlocal sts=2 ts=2 sw=2
        autocmd FileType html setlocal sts=2 ts=2 sw=2
        autocmd FileType cshtml setlocal sts=4 ts=4 sw=4
        autocmd FileType cs setlocal sts=4 ts=4 sw=4
        autocmd FileType md setlocal sts=4 ts=4 sw=4
        autocmd FileType javascript setlocal sts=4 ts=4 sw=4 expandtab
        autocmd BufReadPost *.cshtml set syntax=html
        autocmd BufNewFile,BufRead *.vs,*.fs set ft=glsl
        autocmd FileType html iabbrev <buffer> lorem Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
        autocmd FileType html iabbrev <buffer> HTML <!DOCTYPE html><html><head><title></title></head><body></body></html>
        autocmd FileType html iabbrev <buffer> LINK <link rel="stylesheet" type="text/css" href="">
        autocmd filetype python iabbrev <buffer> dtp dt.p(<CR>"""<CR><BS>""")
augroup END

augroup formatting
autocmd!
autocmd BufWritePre *.sh :normal gg=G''
augroup END

"Showmatch significantly slows down omnicomplete
"when the first match contains parentheses.
set noshowmatch

let g:SuperTabDefaultCompletionType = "<c-n>"
let g:SuperTabClosePreviewOnPopupClose = 1

"don't autoselect first item in omnicomplete, show if only one item (for preview)
"remove preview if you don't want to see any documentation whatsoever.
set completeopt=longest,menuone,preview

"Move the preview window (code documentation) to the bottom of the screen, so it doesn't move the code!
"You might also want to look at the echodoc plugin
set splitbelow

" this setting controls how long to wait (in ms) before fetching type / symbol information.
set updatetime=500
" Remove 'Press Enter to continue' message when type information is longer than one line.
set cmdheight=2

"Don't ask to save when changing buffers (i.e. when jumping to a type definition)
set hidden

let g:jedi#goto_command = "<leader>d"
let g:jedi#goto_assignments_command = "<leader>g"
let g:jedi#goto_definitions_command = "<leader>s"
let g:jedi#documentation_command = "K"
let g:jedi#usages_command = "<leader>n"
let g:jedi#completions_command = "<C-Space>"
let g:jedi#rename_command = "<leader>r"
let g:jedi#completions_enabled = 0
let g:jedi#force_py_version = 3
let g:jedi#show_call_signatures = "0"

nnoremap <leader>l :syntax sync fromstart<CR>

au BufRead,BufNewFile *.g set filetype=antlr3
au BufRead,BufNewFile *.g4 set filetype=antlr4
au BufRead,BufNewFile *.tikz set filetype=tex

if &term =~ '256color'
    " Disable Background Color Erase (BCE) so that color schemes
    " work properly when Vim is used inside tmux and GNU screen.
    set t_ut=
endif

set nocscopeverbose
set cursorcolumn

" NOTE(brendan): netrw is the built-in neovim file browser
let g:netrw_liststyle = 3
let g:netrw_banner = 0
let g:netrw_browse_split = 2
let g:netrw_winsize = 25
let g:javascript_plugin_flow = 1
let g:black_virtualenv = '~/.vim_black'

" In ~/.vim/ftplugin/javascript.vim, or somewhere similar.

" NOTE(brendan): ALE
" Equivalent to the above.
let g:ale_linters = {
\       'cpp': ['clangd'],
\       'cuda': ['clangd'],
\       'css': ['eslint'],
\       'javascript': ['eslint'],
\       'python': ['flake8', 'mypy', 'pylint', 'pylsp'],
\}

" Only run linters named in ale_linters settings.
let g:ale_linters_explicit = 0

" Set this variable to 1 to fix files when you save them.
let g:ale_fix_on_save = 1

let g:ale_fixers = {
\       '*': ['remove_trailing_lines', 'trim_whitespace'],
\       'css': ['prettier'],
\       'html': ['prettier'],
\       'javascript': ['eslint', 'prettier'],
\       'python': ['black'],
\       'cpp': ['clang-format'],
\       'cuda': ['clang-format'],
\}

let g:ale_completion_enabled = 1

let g:ale_completion_delay = 1

let g:ale_lsp_suggestions = 1

nmap <silent> <leader>g <Plug>(ale_go_to_definition)
nmap <silent> <leader>n <Plug>(ale_find_references)
nmap <silent> <leader>s :ALESymbolSearch<space>

au BufRead,BufNewFile *.bib setlocal nocindent

let g:tex_flavor = 'latex'
let g:python3_host_prog = '/home/bduke/miniconda/bin/python'
let g:python_host_prog = ''
let g:loaded_python_provider = 0
