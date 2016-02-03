set nocompatible
source $VIMRUNTIME/vimrc_example.vim
" source $VIMRUNTIME/mswin.vim
" behave mswin

set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=$HOME/vimfiles/bundle/Vundle.vim
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
Plugin 'tpope/vim-sensible'
Plugin 'tpope/vim-surround'
Plugin 'tpope/vim-unimpaired'
Plugin 'chazy/cscope_maps'
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
filetype indent on
syntax on

colorscheme kolor

" No highlight after search on Ctrl+N
nmap <silent> <C-N> :silent noh<CR>

" Set tab stops to be 4 spaces
set tabstop=4
set shiftwidth=4
set expandtab

" Get rid of "O" delay
set noesckeys

" Automatically load skeleton.
au BufNewFile *.cpp 0r C:\work\cpp_header.txt | let IndentStyle = "cpp"

map <Esc> :w<CR>
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

set backupdir=c:\work\vim_backup
set directory=c:\work\vim_backup
set undodir=c:\work\vim_backup

set makeprg=build.bat

noremap <A-1> :make<CR>:cs reset<CR>
noremap <A-2> :cp<CR>
noremap <A-3> :cn<CR>
noremap <A-4> :cs reset<CR>
noremap ,1 :cs kill 0<CR>:cs add cscope.out<CR>

set cino=(0

set cscopequickfix=s-,c-,d-,i-,t-,e-

set textwidth=110

" Custom highlighting
if has("autocmd")
  " Highlight TODO, FIXME, NOTE, etc.
  if v:version > 701
    autocmd Syntax * call matchadd('Todo',  '\W\zs\(TODO\|IMPORTANT\)')
    autocmd Syntax * call matchadd('Debug', '\W\zs\(NOTE\|STUDY\)')
  endif
endif

autocmd BufEnter * :syn sync minlines=1 maxlines=50 ccomment
