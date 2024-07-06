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
Plug 'mbbill/undotree'
Plug 'leafgarland/typescript-vim'
Plug 'pangloss/vim-javascript'
Plug 'lervag/vimtex'
" Plug 'github/copilot.vim'
Plug 'f-person/git-blame.nvim'
Plug 'nvim-lua/plenary.nvim'
Plug 'nvim-telescope/telescope.nvim', { 'tag': '0.1.5' }
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
Plug 'nvim-telescope/telescope-file-browser.nvim'
Plug 'nvim-tree/nvim-web-devicons'
Plug 'neovim/nvim-lspconfig'
Plug 'sindrets/diffview.nvim'
Plug 'rebelot/kanagawa.nvim'
" Package manager.
Plug 'williamboman/mason.nvim'
Plug 'williamboman/mason-lspconfig.nvim'

" All of your Plugins must be added before the following line
call plug#end()            " required
filetype plugin indent on
syntax on

colorscheme kanagawa-dragon

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
        au BufRead,BufNewFile *.g set filetype=antlr3
        au BufRead,BufNewFile *.g4 set filetype=antlr4
        au BufRead,BufNewFile *.tikz set filetype=tex
        au BufRead,BufNewFile *.proto3 set filetype=proto
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

au BufRead,BufNewFile *.bib setlocal nocindent

let g:tex_flavor = 'latex'

" NOTE: git-blame https://github.com/f-person/git-blame.nvim
let g:gitblame_enabled = 1

let g:netrw_winsize = 50

" telescope.nvim
" Find files using Telescope command-line sugar.
nnoremap <leader>fb <cmd>Telescope buffers<cr>
nnoremap <leader>fi <cmd>Telescope file_browser<cr>
nnoremap <leader>ff <cmd>Telescope find_files<cr>
nnoremap <leader>lf <cmd>Telescope find_files find_command=rg,--ignore,--hidden,--files,--glob,!third-party prompt_prefix=🔍<cr>
nnoremap <leader>if <cmd>Telescope find_files no_ignore=true<cr>
nnoremap <leader>fs <cmd>Telescope grep_string<cr>
nnoremap <leader>ls <cmd>Telescope grep_string glob_pattern=!third-party prompt_prefix=🔍<cr>
nnoremap <leader>fh <cmd>Telescope help_tags<cr>
nnoremap <leader>fg <cmd>Telescope live_grep<cr>
nnoremap <leader>fx :Telescope live_grep glob_pattern=
nnoremap <leader>lg <cmd>Telescope live_grep glob_pattern=!third-party prompt_prefix=🔍<cr>
nnoremap <leader>to <cmd>Telescope oldfiles<cr>

lua require('telescope').load_extension('file_browser')
lua require('telescope').setup { pickers = { find_files = { hidden = true } } }
lua require('telescope').setup { pickers = { live_grep = { additional_args = function(opts) return { '--hidden' } end } } }
lua require('telescope').setup { defaults = { file_ignore_patterns = { '.git/' } } }

" Prompt for a subdirectory then call Lua `live_grep()` with the specified
" subdirectory as a search path.
function! LiveGrepInputSubdir()
  let l:prompt = "Enter subdirectory (leave empty for cwd): "
  let l:input = input(l:prompt)
  let subdir = l:input
  if l:input == ''
    execute "lua require('telescope.builtin').live_grep()"
  else
    execute "lua require('telescope.builtin').live_grep({search_dirs = {'" . l:input . "'}})"
  endif
endfunction

nnoremap <leader>fd :call LiveGrepInputSubdir()<CR>

function! LiveGrepIncludeGitignore()
  execute "lua require('telescope.builtin').live_grep({vimgrep_arguments = { 'rg', '--color=never', '--no-heading', '--with-filename', '--line-number', '--column', '--smart-case', '-u' }})"
endfunction

nnoremap <leader>ig :call LiveGrepIncludeGitignore()<CR>

" `live_grep()` in the third-party/torch-mlir directory.
function! LiveGrepTorchMlir()
  execute "lua require('telescope.builtin').live_grep({search_dirs = {'third-party/torch-mlir'}})"
endfunction

nnoremap <leader>tg :call LiveGrepTorchMlir()<CR>
" Find files in the third-party/torch-mlir directory.
nnoremap <leader>tf <cmd>Telescope find_files find_command=rg,--ignore,--hidden,--files,--glob,third-party/torch-mlir/**/* prompt_prefix=🔍<cr>

let g:cpp_clangd_options = '--enable-config=1'

" `live_grep()` in the third-party/llvm-project/mlir directory.
function! LiveGrepMlir()
  execute "lua require('telescope.builtin').live_grep({search_dirs = {'third-party/llvm-project/mlir'}})"
endfunction

nnoremap <leader>mg :call LiveGrepMlir()<CR>
" Find files in the third-party/llvm-project/mlir directory.
nnoremap <leader>mf <cmd>Telescope find_files find_command=rg,--ignore,--hidden,--files,--glob,third-party/llvm-project/mlir/**/* prompt_prefix=🔍<cr>

" mblack
function! RunMBlack()
  let l:jobid = jobstart(['mblack', expand('%')], {'on_exit': 'ReloadBuffer'})
endfunction

function! ReloadBuffer(job_id, data, event)
  if a:event == 'exit' && a:data == 0
    checktime
  endif
endfunction

nnoremap <leader>m :noa w<CR>:call RunMBlack()<CR>

" git-blame.nvim
nnoremap <leader>bl :GitBlameOpenCommitURL<CR>

" change window width
nnoremap + 5<C-w>>
nnoremap _ 5<C-w><

" diffview.nvim keybindings.
nnoremap <leader>dh :DiffviewFileHistory<CR>
nnoremap <leader>dc :DiffviewClose<CR>
nnoremap <leader>df :DiffviewFocusFiles<CR>
nnoremap <leader>do :DiffviewOpen<space>

" Restart crashy LSP.
nnoremap <leader>lr :LspRestart<CR>

" Max line length for syntax highlighting.
set synmaxcol=1000000

" Set clipboard for copy paste.
set clipboard=unnamedplus

" Follow symlinks to appease clangd.
function! FollowSymlink()
  let fname = expand('%:p')
  if getftype(fname) == 'link'
    let resolvedfile = resolve(fname)
    let cur_pos = getcurpos()

    " Close any LSP connections
    if exists('*LspStop')
      call LspStop()
    endif

    " Wipe out the current buffer
    let cur_buf = bufnr('%')
    execute 'bwipeout! ' . cur_buf

    " Edit the resolved file
    execute 'edit ' . fnameescape(resolvedfile)

    " Restore cursor position
    call setpos('.', cur_pos)

    " Restart LSP if it was active
    if exists('*LspStart')
      call LspStart()
    endif

    echom "Followed symlink: " . resolvedfile
  else
    echom "Not a symlink"
  endif
endfunction

command! FollowSymlink call FollowSymlink()

lua << EOF
require("mason").setup()
require("mason-lspconfig").setup()

local lspconfig = require 'lspconfig'

-- Common on_attach function for all LSPs
local function on_attach(client, bufnr)
    local function buf_set_keymap(...) vim.api.nvim_buf_set_keymap(bufnr, ...) end

    -- Key mappings
    local keymap_settings = {
        {'n', '<leader>g', '<cmd>lua vim.lsp.buf.definition()<CR>', { noremap=true, silent=false }},
        {'n', '<leader>h', '<cmd>lua vim.lsp.buf.hover()<CR>', { noremap=true, silent=true }},
        {'n', '<leader>n', '<cmd>lua vim.lsp.buf.references()<CR>', { noremap=true, silent=true }},
        {'n', '<leader>f', '<cmd>lua vim.lsp.buf.formatting()<CR>', { noremap=true, silent=true }},
        {'n', '<leader>s', '<cmd>lua vim.lsp.buf.workspace_symbol()<CR>', { noremap=true, silent=true }},
        {'n', '<leader>rn', '<cmd>lua vim.lsp.buf.rename()<CR>', { noremap=true, silent=true }},
        {'n', '<leader>dn', '<cmd>lua vim.diagnostic.goto_next()<CR>', { noremap=true, silent=true }},
        {'n', '<leader>dp', '<cmd>lua vim.diagnostic.goto_prev()<CR>', { noremap=true, silent=true }},
    }

    -- Applying the key mappings
    for _, keymap in ipairs(keymap_settings) do
        buf_set_keymap(unpack(keymap))
    end
end

-- Setup LSPs with common configurations
local servers = {'bzl', 'clangd', 'jedi_language_server', 'marksman', 'mojo', 'pylsp', 'pyright'}
for _, lsp in ipairs(servers) do
    lspconfig[lsp].setup { on_attach = on_attach }
end

local util = require 'lspconfig.util'

local modular_path = os.getenv("MODULAR_PATH")
local bazelw = modular_path .. "/bazelw"

lspconfig.mojo.setup {
  cmd = {
    bazelw,
    'run', '//KGEN/tools/mojo-lsp-server'
  },
  filetypes = { 'mojo' },
  root_dir = util.find_git_ancestor,
  single_file_support = true,
  on_attach = on_attach,
}

--- Set up Bazel LSP.
local bazel_lsp = "/home/ubuntu/.cache/bazel/_bazel_ubuntu/dcddefca2a2b2bd8462a64e331af35cd/execroot/_main/bazel-out/aarch64-opt/bin/bazel-lsp"

lspconfig.bzl.setup {
  cmd = {
    bazel_lsp,
  },
  filetypes = { 'bzl' },
  root_dir = util.find_git_ancestor,
  single_file_support = true,
  on_attach = on_attach,
}

vim.api.nvim_create_autocmd("BufWritePre", {
    buffer = buffer,
    pattern = {"*.cpp", "*.hpp", "*.c", "*.h", ".cc", ".hh", ".cxx", ".hxx", "*.py", "*.sh"},
    callback = function()
        vim.lsp.buf.format { async = false }
    end
})

vim.api.nvim_create_autocmd("BufWritePost", {
    pattern = {"*.mojo", "*.🔥"},
    callback = function()
        -- Save the current cursor position
        local cursor_pos = vim.api.nvim_win_get_cursor(0)
        -- Get the current buffer's file name
        local file = vim.fn.expand('%:p')
        -- Run mblack on the file
        vim.cmd('silent! !mblack ' .. file)
        -- Restore the cursor position
        vim.api.nvim_win_set_cursor(0, cursor_pos)
    end
})

-- Enable relative line numbers.
vim.wo.relativenumber = true
EOF
