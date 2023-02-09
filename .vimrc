let mapleader = '-'

set nocompatible              " be iMproved, required
filetype off                  " required

call plug#begin()
" The default plugin directory will be as follows:
"   - Vim (Linux/macOS): '~/.vim/plugged'
"   - Vim (Windows): '~/vimfiles/plugged'
"   - Neovim (Linux/macOS/Windows): stdpath('data') . '/plugged'
" You can specify a custom plugin directory by passing it as the argument
"   - e.g. `call plug#begin('~/.vim/plugged')`
"   - Avoid using standard Vim directory names like 'plugin'

Plug 'tpope/vim-commentary'
Plug 'tpope/vim-dispatch'
Plug 'tpope/vim-fugitive'
Plug 'tpope/vim-git'
Plug 'tpope/vim-surround'
Plug 'tpope/vim-unimpaired'
Plug 'myusuf3/numbers.vim'
Plug 'zeis/vim-kolor'
Plug 'flazz/vim-colorschemes'
" NOTE(brendan): jedi-vim can sometimes get into a state where it lags a lot,
" apparently requiring system reboot to resolve
" Seems to go away with let g:jedi#show_call_signatures = "0"
" See this thread: https://github.com/davidhalter/jedi-vim/issues/217
Plug 'davidhalter/jedi-vim'
Plug 'dylon/vim-antlr'
Plug 'yegappan/mru'
Plug 'mbbill/undotree'
Plug 'leafgarland/typescript-vim'
Plug 'psf/black'
Plug 'pangloss/vim-javascript'
Plug 'dense-analysis/ale'
Plug 'lervag/vimtex'
Plug 'ervandew/supertab'
Plug 'github/copilot.vim'
Plug 'f-person/git-blame.nvim'
Plug 'nvim-lua/plenary.nvim'
Plug 'nvim-telescope/telescope.nvim', {'tag': '0.1.1'}
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
Plug 'nvim-telescope/telescope-file-browser.nvim'
Plug 'nvim-tree/nvim-web-devicons'

" All of your Plugins must be added before the following line
call plug#end()            " required
filetype plugin indent on
syntax on

colorscheme kolor

" No highlight after search on Ctrl+N
nmap <silent> <C-N> :silent noh<CR>

" Set tab stops to be 2 spaces
set tabstop=2
set softtabstop=2
set shiftwidth=2
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
        autocmd FileType go setlocal sts=2 ts=2 sw=2 noexpandtab
        autocmd BufReadPost *.cshtml set syntax=html
        autocmd BufNewFile,BufRead *.vs,*.fs set ft=glsl
        autocmd FileType html iabbrev <buffer> lorem Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
        autocmd FileType html iabbrev <buffer> HTML <!DOCTYPE html><html><head><title></title></head><body></body></html>
        autocmd FileType html iabbrev <buffer> LINK <link rel="stylesheet" type="text/css" href="">
        autocmd filetype python iabbrev <buffer> dtp dt.p(<CR>"""<CR><BS>""")
        autocmd BufNewFile,BufRead *.h.inc,*.cpp.inc set ft=cpp
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
" TODO: pylsp
let g:ale_linters = {
\       'cmake': ['cmake-language-server'],
\       'c': ['clangd'],
\       'cpp': ['clangd', 'clangtidy', 'clang'],
\       'cuda': ['clangd'],
\       'css': ['eslint'],
\       'javascript': ['eslint'],
\       'python': ['mypy', 'flake8', 'pylint', 'pyright'],
\       'tablegen': ['clangd'],
\}
" Only run linters named in ale_linters settings.
let g:ale_linters_explicit = 0
" Set this variable to 1 to fix files when you save them.
let g:ale_fix_on_save = 1
let g:ale_fixers = {
\       '*': ['remove_trailing_lines', 'trim_whitespace'],
\       'css': ['prettier'],
\       'go': ['gofmt'],
\       'html': ['prettier'],
\       'javascript': ['eslint', 'prettier-eslint'],
\       'python': ['black', 'isort'],
\       'cpp': ['clang-format', 'clangtidy'],
\       'cuda': ['clang-format'],
\       'c': ['clang-format'],
\       'tex': ['latexindent'],
\}
let g:ale_completion_enabled = 0
let g:ale_completion_delay = 100
let g:ale_lsp_suggestions = 1

nmap <silent> <leader>g <Plug>(ale_go_to_definition)
nmap <silent> <leader>d <Plug>(ale_go_to_implementation)
nmap <silent> <leader>n <Plug>(ale_find_references)
nmap <silent> <leader>s :ALESymbolSearch<space>

au BufRead,BufNewFile *.bib setlocal nocindent

let g:tex_flavor = 'latex'

" NOTE: git-blame https://github.com/f-person/git-blame.nvim
let g:gitblame_enabled = 1

let g:netrw_winsize = 50

let g:ale_python_flake8_options = '--max-line-length=80'

" telescope.nvim
" Find files using Telescope command-line sugar.
nnoremap <leader>fb <cmd>Telescope buffers<cr>
nnoremap <leader>fi <cmd>Telescope file_browser<cr>
nnoremap <leader>ff <cmd>Telescope find_files<cr>
nnoremap <leader>lf <cmd>Telescope find_files find_command=rg,--ignore,--hidden,--files,--glob,!third-party prompt_prefix=🔍<cr>
nnoremap <leader>fs <cmd>Telescope grep_string<cr>
nnoremap <leader>fh <cmd>Telescope help_tags<cr>
nnoremap <leader>fg <cmd>Telescope live_grep<cr>
nnoremap <leader>lg <cmd>Telescope live_grep glob_pattern=!third-party prompt_prefix=🔍<cr>

lua require('telescope').load_extension('file_browser')
lua require('telescope').setup { pickers = { find_files = { hidden = true } } }
lua require('telescope').setup { pickers = { live_grep = { additional_args = function(opts) return { '--hidden' } end } } }
