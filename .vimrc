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
" Plugin 'tpope/vim-sensible'
Plugin 'tpope/vim-surround'
Plugin 'tpope/vim-unimpaired'
" Plugin 'Valloric/YouCompleteMe'
Plugin 'chazy/cscope_maps'
Plugin 'lyuts/vim-rtags'
Plugin 'tpope/vim-dispatch'
Plugin 'Shougo/unite.vim'
Plugin 'davidhalter/jedi-vim'
Plugin 'dylon/vim-antlr'
Plugin 'pangloss/vim-javascript'
Plugin 'neomake/neomake'
Plugin 'yegappan/mru'
Plugin 'mbbill/undotree'
Plugin 'keith/swift.vim'
Plugin 'leafgarland/typescript-vim'

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
"filetype plugin on
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

" Disable auto-comments
autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o

" matchit.vim
runtime macros/matchit.vim

" YCM recognizes ctags files
let g:ycm_collect_identifiers_from_tags_files = 1

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

"autocmd BufRead,BufNewFile *.md,*.c,*.h,*.java set noexpandtab

set cino+=(0

autocmd BufEnter * :syn sync minlines=400 maxlines=400 ccomment
autocmd BufEnter *.py :syn sync fromstart
autocmd FileType latex set sts=0 ts=0 sw=0
autocmd FileType html setlocal sts=4 ts=4 sw=4
autocmd FileType cshtml setlocal sts=4 ts=4 sw=4
autocmd FileType cs setlocal sts=4 ts=4 sw=4
autocmd FileType md setlocal sts=4 ts=4 sw=4
autocmd FileType cs noremap ,1 :!gen_aspnet_cscope.sh<CR>:cs reset<CR>
au BufReadPost *.cshtml set syntax=html

"Showmatch significantly slows down omnicomplete
"when the first match contains parentheses.
set noshowmatch

"Super tab settings - uncomment the next 4 lines
"let g:SuperTabDefaultCompletionType = 'context'
"let g:SuperTabContextDefaultCompletionType = "<c-x><c-o>"
"let g:SuperTabDefaultCompletionTypeDiscovery = ["&omnifunc:<c-x><c-o>","&completefunc:<c-x><c-n>"]
"let g:SuperTabClosePreviewOnPopupClose = 1

"don't autoselect first item in omnicomplete, show if only one item (for preview)
"remove preview if you don't want to see any documentation whatsoever.
set completeopt=longest,menuone,preview

"Move the preview window (code documentation) to the bottom of the screen, so it doesn't move the code!
"You might also want to look at the echodoc plugin
set splitbelow

" Get Code Issues and syntax errors
let g:syntastic_cs_checkers = ['syntax', 'semantic', 'issues']

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

let g:syntastic_check_on_open = 0
let g:syntastic_check_on_wq = 1

nnoremap <leader>l :syntax sync fromstart<CR>

au BufRead,BufNewFile *.g set filetype=antlr3
au BufRead,BufNewFile *.g4 set filetype=antlr4
au BufRead,BufNewFile *.tikz set filetype=tex

autocmd! BufWritePost * Neomake

if &term =~ '256color'
    " Disable Background Color Erase (BCE) so that color schemes
    " work properly when Vim is used inside tmux and GNU screen.
    set t_ut=
endif

let g:neomake_python_exe = 'python3'
set nocscopeverbose
set cursorcolumn

let g:netrw_liststyle = 3
let g:netrw_banner = 0
let g:netrw_browse_split = 2
let g:netrw_winsize = 25
let g:javascript_plugin_flow = 1
