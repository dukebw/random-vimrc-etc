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
Plug 'nvim-telescope/telescope.nvim', { 'tag': '0.1.8' }
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
Plug 'nvim-telescope/telescope-file-browser.nvim'
Plug 'nvim-telescope/telescope-live-grep-args.nvim'
Plug 'nvim-tree/nvim-web-devicons'
Plug 'neovim/nvim-lspconfig'
Plug 'sindrets/diffview.nvim'
Plug 'rebelot/kanagawa.nvim'
" Package manager.
Plug 'williamboman/mason.nvim'
Plug 'williamboman/mason-lspconfig.nvim'
" Semantic highlighting for Python.
Plug 'wookayin/semshi', { 'do': ':UpdateRemotePlugins', 'tag': '*' }
" nvim debugger
Plug 'mfussenegger/nvim-dap'
Plug 'nvim-neotest/nvim-nio'
Plug 'rcarriga/nvim-dap-ui'
Plug 'theHamsta/nvim-dap-virtual-text'
Plug 'mfussenegger/nvim-dap-python'
Plug 'nvimtools/none-ls.nvim'

" nvim-cmp
Plug 'hrsh7th/cmp-nvim-lsp'
Plug 'hrsh7th/cmp-buffer'
Plug 'hrsh7th/cmp-path'
Plug 'hrsh7th/cmp-cmdline'
Plug 'hrsh7th/nvim-cmp'

" For vsnip users.
Plug 'hrsh7th/cmp-vsnip'
Plug 'hrsh7th/vim-vsnip'

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

" Set the Python3 provider.
let g:python3_host_prog = "python"

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

if &term =~ '256color'
    " Disable Background Color Erase (BCE) so that color schemes
    " work properly when Vim is used inside tmux and GNU screen.
    set t_ut=
endif

set cursorcolumn

" NOTE(brendan): netrw is the built-in neovim file browser
let g:netrw_liststyle = 3
let g:netrw_banner = 0
let g:netrw_browse_split = 0
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

" Find files in the bazel-out directory.
nnoremap <leader>bzf <cmd>Telescope find_files find_command=rg,--follow,-uuu,--hidden,--files,--glob,bazel-out/aarch64-opt-sane-release/bin/**/*.inc prompt_prefix=🔍<cr>

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
nnoremap <leader>+ 5<C-w>+
nnoremap <leader>_ 5<C-w>-

" diffview.nvim keybindings.
nnoremap <leader>dh :DiffviewFileHistory<CR>
nnoremap <leader>dc :DiffviewClose<CR>
nnoremap <leader>df :DiffviewFocusFiles<CR>
nnoremap <leader>do :DiffviewOpen<space>

" Restart crashy LSP.
nnoremap <leader>lr :LspRestart<CR>

" Max line length for syntax highlighting.
set synmaxcol=1000000

set clipboard=unnamedplus

" Follow symlinks to appease clangd.
function! FollowSymlink()
  let fname = expand('%:p')
  if getftype(fname) == 'link'
    let resolvedfile = resolve(fname)
    let cur_win = winnr()
    let cur_pos = getcurpos()

    " Store information about all windows
    let win_info = []
    windo call add(win_info, [winnr(), bufname('%'), getcurpos()])

    " Go back to the original window
    execute cur_win . 'wincmd w'

    " Edit the resolved file
    execute 'keepalt edit ' . fnameescape(resolvedfile)

    " Restore cursor position
    call setpos('.', cur_pos)

    " Restore all other windows
    for [win, bufname, pos] in win_info
      if win != cur_win
        execute win . 'wincmd w'
        if bufname != resolvedfile
          execute 'buffer ' . bufname
          call setpos('.', pos)
        endif
      endif
    endfor

    " Go back to the original window
    execute cur_win . 'wincmd w'

    " Update the buffer name to the resolved file
    execute 'file ' . fnameescape(resolvedfile)

    " Refresh buffer to ensure it's linked to the correct file
    edit

    if exists('b:lsp_connected')
      LspRestart
    endif

    echom "Followed symlink: " . resolvedfile
  else
    echom "Not a symlink"
  endif
endfunction

command! FollowSymlink call FollowSymlink()

nnoremap <leader>sy :FollowSymlink<CR>

" Override Semshi semantic highlighting colours.
function! MyCustomHighlights()
  " I changed guifg over to kanagawa.nvim/lua/kanagawa/colors.lua.
  " Whatever was closest.
  hi semshiLocal           ctermfg=209 guifg=#ff875f
  hi semshiGlobal          ctermfg=214 guifg=#8992a7
  hi semshiImported        ctermfg=214 guifg=#87a987 cterm=bold gui=bold
  hi semshiParameter       ctermfg=75  guifg=#a6a69c
  hi semshiParameterUnused ctermfg=117 guifg=#737c73 cterm=underline gui=underline
  hi semshiFree            ctermfg=218 guifg=#e82424
  hi semshiBuiltin         ctermfg=207 guifg=#c4746e
  hi semshiAttribute       ctermfg=49  guifg=#c4b28a
  hi semshiSelf            ctermfg=249 guifg=#949fb5
  hi semshiUnresolved      ctermfg=226 guifg=#f2ecbc cterm=underline gui=underline
  hi semshiSelected        ctermfg=231 guifg=#f9d791 ctermbg=161 guibg=#d7005f

  hi semshiErrorSign       ctermfg=231 guifg=#FFA066 ctermbg=160 guibg=#d70000
  hi semshiErrorChar       ctermfg=231 guifg=#FFA066 ctermbg=160 guibg=#d70000
  sign define semshiError text=E> texthl=semshiErrorSign
endfunction
autocmd FileType python call MyCustomHighlights()

let g:semshi#always_update_all_highlights = v:true
let g:semshi#update_delay_factor = 0.0001

" Copies current relative filepath.
nnoremap <silent> <leader>cp :let @+ = expand('%') \| echo 'Copied: ' . @+<CR>

lua << EOF
require("mason").setup()
require("mason-lspconfig").setup()

local lspconfig = require 'lspconfig'

-- Common on_attach function for all LSPs.
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

-- Set up nvim-cmp.
-- https://github.com/hrsh7th/nvim-cmp
local cmp = require'cmp'

cmp.setup({
  snippet = {
    -- REQUIRED - you must specify a snippet engine
    expand = function(args)
      vim.fn["vsnip#anonymous"](args.body) -- For `vsnip` users.
      -- require('luasnip').lsp_expand(args.body) -- For `luasnip` users.
      -- require('snippy').expand_snippet(args.body) -- For `snippy` users.
      -- vim.fn["UltiSnips#Anon"](args.body) -- For `ultisnips` users.
      -- vim.snippet.expand(args.body) -- For native neovim snippets (Neovim v0.10+)
    end,
  },
  window = {
    -- completion = cmp.config.window.bordered(),
    -- documentation = cmp.config.window.bordered(),
  },
  mapping = cmp.mapping.preset.insert({
    ['<C-b>'] = cmp.mapping.scroll_docs(-4),
    ['<C-f>'] = cmp.mapping.scroll_docs(4),
    ['<C-Space>'] = cmp.mapping.complete(),
    ['<C-e>'] = cmp.mapping.abort(),
    ['<Tab>'] = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.select_next_item() -- Tab to select the next item
      else
        fallback() -- If no suggestions, fallback to default Tab behavior
      end
    end, { "i", "s" }),
    ['<S-Tab>'] = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.select_prev_item() -- Shift+Tab to select the previous item
      else
        fallback() -- If no suggestions, fallback to default Shift+Tab behavior
      end
    end, { "i", "s" }),
    ['<CR>'] = cmp.mapping.confirm({ select = true }), -- Accept currently selected item. Set `select` to `false` to only confirm explicitly selected items.
  }),
  sources = cmp.config.sources({
    { name = 'nvim_lsp' },
    { name = 'vsnip' }, -- For vsnip users.
    -- { name = 'luasnip' }, -- For luasnip users.
    -- { name = 'ultisnips' }, -- For ultisnips users.
    -- { name = 'snippy' }, -- For snippy users.
  }, {
    { name = 'buffer' },
  })
})

-- To use git you need to install the plugin petertriho/cmp-git and uncomment lines below
-- Set configuration for specific filetype.
--[[ cmp.setup.filetype('gitcommit', {
  sources = cmp.config.sources({
    { name = 'git' },
  }, {
    { name = 'buffer' },
  })
)
require("cmp_git").setup() ]]-- 

-- Use buffer source for `/` and `?` (if you enabled `native_menu`, this won't work anymore).
cmp.setup.cmdline({ '/', '?' }, {
  mapping = cmp.mapping.preset.cmdline(),
  sources = {
    { name = 'buffer' }
  }
})

-- Use cmdline & path source for ':' (if you enabled `native_menu`, this won't work anymore).
cmp.setup.cmdline(':', {
  mapping = cmp.mapping.preset.cmdline(),
  sources = cmp.config.sources({
    { name = 'path' }
  }, {
    { name = 'cmdline' }
  }),
  matching = { disallow_symbol_nonprefix_matching = false }
})

-- Set up lspconfig.
local capabilities = require('cmp_nvim_lsp').default_capabilities()

-- Set up LSPs with common configurations.
local servers = {'bzl', 'clangd', 'marksman', 'mojo', 'vimls', 'yamlls'}
for _, lsp in ipairs(servers) do
    lspconfig[lsp].setup { on_attach = on_attach, capabilities = capabilities }
end

local modular_path = os.getenv("MODULAR_PATH")
local api_generated_pkgs = vim.fn.expand("$MODULAR_PATH/bazel-bin/SDK/lib/API/python")
local api_source_pkgs = vim.fn.expand("$MODULAR_PATH/SDK/lib/API/python")
local pipelines_source_pkgs = vim.fn.expand("$MODULAR_PATH/SDK/public/max-repo/pipelines/python")
local pipelines_venv = vim.fn.expand("$MODULAR_PATH/.SDK+public+max-repo+pipelines+python+pipelines.venv")
local python_exe = pipelines_venv .. "/bin/python"
local ruff_exe = pipelines_venv .. "/bin/ruff"

-- Set MYPYPATH
vim.env.MYPYPATH = "external/rules_python~~pip~modular_pip_deps_311_click/site-packages:external/rules_python~~pip~modular_pip_deps_311_click/site-packages:external/rules_python~~pip~modular_pip_deps_311_huggingface_hub/site-packages:external/rules_python~~pip~modular_pip_deps_311_filelock/site-packages:external/rules_python~~pip~modular_pip_deps_311_fsspec/site-packages:external/rules_python~~pip~modular_pip_deps_311_packaging/site-packages:external/rules_python~~pip~modular_pip_deps_311_pyyaml/site-packages:external/rules_python~~pip~modular_pip_deps_311_certifi/site-packages:external/rules_python~~pip~modular_pip_deps_311_charset_normalizer/site-packages:external/rules_python~~pip~modular_pip_deps_311_idna/site-packages:external/rules_python~~pip~modular_pip_deps_311_urllib3/site-packages:external/rules_python~~pip~modular_pip_deps_311_requests/site-packages:external/rules_python~~pip~modular_pip_deps_311_tqdm/site-packages:external/rules_python~~pip~modular_pip_deps_311_huggingface_hub/site-packages:external/rules_python~~pip~modular_pip_deps_311_hypothesis/site-packages:external/rules_python~~pip~modular_pip_deps_311_attrs/site-packages:external/rules_python~~pip~modular_pip_deps_311_sortedcontainers/site-packages:external/rules_python~~pip~modular_pip_deps_311_hypothesis/site-packages:external/rules_python~~pip~modular_pip_deps_311_pytest_asyncio/site-packages:external/rules_python~~pip~modular_pip_deps_311_iniconfig/site-packages:external/rules_python~~pip~modular_pip_deps_311_packaging/site-packages:external/rules_python~~pip~modular_pip_deps_311_pluggy/site-packages:external/rules_python~~pip~modular_pip_deps_311_pytest/site-packages:external/rules_python~~pip~modular_pip_deps_311_pytest_asyncio/site-packages:external/rules_python~~pip~modular_pip_deps_311_pytest_xdist/site-packages:external/rules_python~~pip~modular_pip_deps_311_execnet/site-packages:external/rules_python~~pip~modular_pip_deps_311_iniconfig/site-packages:external/rules_python~~pip~modular_pip_deps_311_packaging/site-packages:external/rules_python~~pip~modular_pip_deps_311_pluggy/site-packages:external/rules_python~~pip~modular_pip_deps_311_pytest/site-packages:external/rules_python~~pip~modular_pip_deps_311_pytest_xdist/site-packages:external/rules_python~~pip~modular_pip_deps_311_torch/site-packages:external/rules_python~~pip~modular_pip_deps_311_filelock/site-packages:external/rules_python~~pip~modular_pip_deps_311_fsspec/site-packages:external/rules_python~~pip~modular_pip_deps_311_markupsafe/site-packages:external/rules_python~~pip~modular_pip_deps_311_jinja2/site-packages:external/rules_python~~pip~modular_pip_deps_311_networkx/site-packages:external/rules_python~~pip~modular_pip_deps_311_mpmath/site-packages:external/rules_python~~pip~modular_pip_deps_311_sympy/site-packages:external/rules_python~~pip~modular_pip_deps_311_torch/site-packages:external/rules_python~~pip~modular_pip_deps_311_transformers/site-packages:external/rules_python~~pip~modular_pip_deps_311_filelock/site-packages:external/rules_python~~pip~modular_pip_deps_311_fsspec/site-packages:external/rules_python~~pip~modular_pip_deps_311_packaging/site-packages:external/rules_python~~pip~modular_pip_deps_311_pyyaml/site-packages:external/rules_python~~pip~modular_pip_deps_311_certifi/site-packages:external/rules_python~~pip~modular_pip_deps_311_charset_normalizer/site-packages:external/rules_python~~pip~modular_pip_deps_311_idna/site-packages:external/rules_python~~pip~modular_pip_deps_311_urllib3/site-packages:external/rules_python~~pip~modular_pip_deps_311_requests/site-packages:external/rules_python~~pip~modular_pip_deps_311_tqdm/site-packages:external/rules_python~~pip~modular_pip_deps_311_huggingface_hub/site-packages:external/rules_python~~pip~modular_pip_deps_311_numpy/site-packages:external/rules_python~~pip~modular_pip_deps_311_regex/site-packages:external/rules_python~~pip~modular_pip_deps_311_safetensors/site-packages:external/rules_python~~pip~modular_pip_deps_311_tokenizers/site-packages:external/rules_python~~pip~modular_pip_deps_311_transformers/site-packages:external/rules_python~~pip~modular_pip_deps_311_pytest/site-packages:external/rules_python~~pip~modular_pip_deps_311_iniconfig/site-packages:external/rules_python~~pip~modular_pip_deps_311_packaging/site-packages:external/rules_python~~pip~modular_pip_deps_311_pluggy/site-packages:external/rules_python~~pip~modular_pip_deps_311_pytest/site-packages:external/rules_python~/site-packages:external/rules_python~:site-packages:SDK/integration-test/pipelines/python:SDK/lib/API/python:SDK/public/max-repo/pipelines/python:rules_python~:SDK/integration-test/pipelines/python/test_common:SDK/integration-test/pipelines/python/llama3:SDK/integration-test/API/python/graph_tests:Support/python:bazel-out/k8-opt-release/bin:bazel-out/k8-opt-release/bin/site-packages:bazel-out/k8-opt-release/bin/SDK/integration-test/pipelines/python:bazel-out/k8-opt-release/bin/SDK/lib/API/python:bazel-out/k8-opt-release/bin/SDK/public/max-repo/pipelines/python:bazel-out/k8-opt-release/bin/rules_python~:bazel-out/k8-opt-release/bin/SDK/integration-test/pipelines/python/test_common:bazel-out/k8-opt-release/bin/SDK/integration-test/pipelines/python/llama3:bazel-out/k8-opt-release/bin/SDK/integration-test/API/python/graph_tests:bazel-out/k8-opt-release/bin/Support/python:SDK/integration-test/pipelines/python/llama3/testdata:/home/ubuntu/.cache/bazel/_bazel_ubuntu/a5171e680520db7be14c4ce5f82e546f/execroot/_main/bazel-out/k8-fastbuild-default/bin/SDK/public/max-repo/pipelines/python/pipelines.venv.runfiles/_main/SDK/lib/API/python"

lspconfig.pylsp.setup {
    cmd = { python_exe, '-m', 'pylsp' },
    on_attach = on_attach,
    settings = {
        pylsp = {
            plugins = {
               ruff = {
                  enabled = true,  -- Enable the plugin
                  formatEnabled = true,  -- Enable formatting using ruffs formatter
                  executable = ruff_exe,  -- Custom path to ruff
                  -- config = "<path_to_custom_ruff_toml>",  -- Custom config for ruff to use
                  extendSelect = { "I" },  -- Rules that are additionally used by ruff
                  -- extendIgnore = { "C90" },  -- Rules that are additionally ignored by ruff
                  format = { "I" },  -- Rules that are marked as fixable by ruff that should be fixed when running textDocument/formatting
                  -- severities = { ["D212"] = "I" },  -- Optional table of rules where a custom severity is desired
                  unsafeFixes = true,  -- Whether or not to offer unsafe fixes as code actions. Ignored with the "Fix All" action

                  -- Rules that are ignored when a pyproject.toml or ruff.toml is present:
                  lineLength = 80,  -- Line length to pass to ruff checking and formatting
                  -- exclude = { "__about__.py" },  -- Files to be excluded by ruff checking
                  select = { "ALL" },  -- Rules to be enabled by ruff
                  -- Rules to be ignored by ruff:
                  -- D401: imperative docstring.
                  -- D410: blank line after Returns: in docstring.
                  -- COM812: trailing comma missing.
                  -- TD003: missing issue link on the line following this TODO.
                  ignore = { "D401", "D413", "COM812", "TD003" },
                  perFileIgnores = { ["__init__.py"] = {"F401"} },  -- Rules that should be ignored for specific files
                  preview = false,  -- Whether to enable the preview style linting and formatting.
                  targetVersion = "py39",  -- The minimum python version to target (applies for both linting and formatting).
                },
                jedi = {
                  environment = python_exe,
                  -- extra_paths = {
                  --   api_generated_pkgs,
                  --   api_source_pkgs,
                  --   pipelines_source_pkgs,
                  -- },
                },
                -- Type checking.
                pylsp_mypy = {
                  enabled = true,
                  live_mode = false,
                  report_progress = false,
                  config = modular_path .. "/mypy.ini",
                  -- dmypy = true,
                },
                pylint = {
                  enabled = false  -- Disable pylint to avoid conflicts
                },
                -- import sorting
                isort = { enabled = true },
            },
        },
    },
    flags = {
      debounce_text_changes = 200,
    },
}

lspconfig.mlir_lsp_server.setup {
  on_attach = on_attach,
  cmd = {
    'modular-lsp-server',
  },
  filetypes = {
    'mlir',
  },
}

lspconfig.tblgen_lsp_server.setup {
  on_attach = on_attach,
  cmd = {
    'tblgen-lsp-server',
    '--tablegen-compilation-database=.derived/build/tablegen_compile_commands.yml',
  },
}

-- vim.lsp.set_log_level("debug")

local util = require 'lspconfig.util'

local max = modular_path .. "/SDK/lib/API/mojo/max"
local pipelines = modular_path .. "/SDK/public/max-repo/examples/graph-api"
local examples = modular_path .. "/ModularFramework/examples"
local examples_pipelines = examples .. "/pipelines"
local kernels = modular_path .. "/Kernels/mojo"
local kernels_test = modular_path .. "/Kernels/test"
local extensibility = modular_path .. "/Kernels/mojo/extensibility"
local stdlib = modular_path .. "/open-source/mojo/stdlib/stdlib"

lspconfig.mojo.setup {
  cmd = {
    'mojo-lsp-server',
    '-I', kernels,
    '-I', max,
    '-I', pipelines,
    '-I', kernels_test,
    '-I', extensibility,
    -- '-I', stdlib,
  },
  filetypes = { 'mojo' },
  root_dir = util.find_git_ancestor,
  single_file_support = true,
  on_attach = on_attach,
  capabilities = capabilities
}

--- Set up Bazel LSP.
local bazel_lsp = "/home/ubuntu/work/bazel-lsp/bazel-bin/bazel-lsp"
local bazelrc_lsp = "/home/ubuntu/work/bazelrc-lsp/vscode-extension/dist/bazelrc-lsp"

lspconfig.bzl.setup {
  cmd = {
    bazel_lsp,
  },
  filetypes = { 'bzl' },
  root_dir = util.find_git_ancestor,
  single_file_support = true,
  on_attach = on_attach,
}

vim.filetype.add {
  pattern = {
    ['.*.bazelrc'] = 'bazelrc',
  },
}

lspconfig.bazelrc_lsp.setup {
  cmd = {
    bazelrc_lsp,
  },
  filetypes = { 'bazelrc' },
  on_attach = on_attach,
}

local null_ls = require("null-ls")

null_ls.setup({
    sources = {
        null_ls.builtins.formatting.buildifier,
    },
})

vim.api.nvim_create_autocmd("BufWritePre", {
    buffer = buffer,
    pattern = {"*.cpp", "*.hpp", "*.c", "*.h", ".cc", ".hh", ".cxx", ".hxx", "*.py", "*.sh", "BUILD", "WORKSPACE", "*.bazel", "*.bzl"},
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

-- nvim-dap:
-- https://github.com/mfussenegger/nvim-dap/wiki/Debug-Adapter-installation#ccrust-via-lldb-vscode
local dap = require('dap')
dap.set_log_level('DEBUG')
local dapui = require('dapui')

dap.listeners.after.event_initialized["dapui_config"] = function()
  dapui.open()
end
-- dap.listeners.before.event_terminated["dapui_config"] = function()
--   dapui.close()
-- end
-- dap.listeners.before.event_exited["dapui_config"] = function()
--   dapui.close()
-- end

dap.adapters.lldb = {
  type = 'executable',
  command = '/usr/bin/lldb-dap', -- must be absolute path
  name = 'lldb'
}

-- Configure C++ DAP.
local function read_json_config(file_path)
  local file = io.open(file_path, "r")
  if not file then
    print("Config file not found: " .. file_path)
    return nil
  end

  local content = file:read("*all")
  file:close()

  local status, config = pcall(vim.fn.json_decode, content)
  if not status then
    print("Error parsing JSON config: " .. config)
    return nil
  end

  return config
end

local function get_config_or_input(config, key, prompt, default)
  if config and config[key] then
    return config[key]
  else
    return vim.fn.input(prompt, default or '')
  end
end

local function merge_environments(default_env, json_env)
  local merged_env = vim.deepcopy(default_env)
  if json_env then
    for k, v in pairs(json_env) do
      merged_env[k] = v
    end
  end
  return merged_env
end

-- Gets configuration from .nvim-dap.json, or nil.
local function get_config_value(key)
  local config = read_json_config(vim.fn.getcwd() .. '/.nvim-dap.json')
  if config then
    return config[key]
  end
  return nil
end

-- Determines program or pytest execution.
local function determine_program()
  if get_config_value('run_with_pytest') then
    return nil
  end

  return get_config_value('python_file') or "${file}"
end

-- Constructs pytest args.
local function build_pytest_args()
  local args = get_config_value('args') or {}
  if get_config_value('run_with_pytest') and get_config_value('test_function') then
    if #args > 0 then
      args[#args] = args[#args] .. "::" .. get_config_value('test_function')
    end
  end
  return args
end

local default_env = {}

dap.configurations.cpp = {
  {
    name = 'Launch',
    type = 'lldb',
    request = 'launch',
    program = function()
      local config = read_json_config(vim.fn.getcwd() .. '/.nvim-dap.json')
      return get_config_or_input(config, "program", 'Path to executable: ', vim.fn.getcwd() .. '/')
    end,
    cwd = '${workspaceFolder}',
    stopOnEntry = false,
    args = function()
      local config = read_json_config(vim.fn.getcwd() .. '/.nvim-dap.json')
      if config and config.cpp_args then
        return config.cpp_args
      else
        local input = vim.fn.input('Args: ')
        return vim.split(input, " ")
      end
    end,
    justMyCode = false,
    env = function()
      local config = read_json_config(vim.fn.getcwd() .. '/.nvim-dap.json')
      return merge_environments(default_env, config and config.env or nil)
    end,
    initCommands = function()
      local env = dap.configurations.cpp[1].env()
      local commands = {}
      for k, v in pairs(env) do
        table.insert(commands, string.format('settings set target.env-vars %s="%s"', k, v))
      end
      return commands
    end,

    -- 💀
    -- if you change `runInTerminal` to true, you might need to change the yama/ptrace_scope setting:
    --
    --    echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
    --
    -- Otherwise you might get the following error:
    --
    --    Error on launch: Failed to attach to the target process
    --
    -- But you should be aware of the implications:
    -- https://www.kernel.org/doc/html/latest/admin-guide/LSM/Yama.html
    -- runInTerminal = false,
  },
  {
    name = 'Attach to Process',
    type = 'lldb',
    request = 'attach',
    pid = require('dap.utils').pick_process,
    cwd = '${workspaceFolder}',
    justMyCode = false,
  },
}

-- Configure Python DAP.
dap.adapters.python = function(callback, config)
  if config.request == 'attach' then
    -- Attach to an existing debugpy instance.
    callback({
      type = 'server',
      host = (config.connect or config).host or '127.0.0.1',
      port = (config.connect or config).port or 5678,
      options = {
        source_filetype = 'python',
      },
    })
  else
    -- Launch a new debugpy instance.
    callback({
      type = 'executable',
      command = 'python',
      args = { '-m', 'debugpy.adapter' },
      options = {
        source_filetype = 'python',
      },
    })
  end
end

require("dap-python").setup("/home/ubuntu/work/modular/.SDK+public+max-repo+pipelines+python+pipelines.venv/bin/python")
require('dap-python').test_runner = 'pytest'
-- python -m debugpy --version must work in the shell.

-- Loop over all Python configurations and set justMyCode to false
for _, config in ipairs(dap.configurations.python) do
  config.justMyCode = false
end

-- nvim dap UI
dapui.setup()
require("nvim-dap-virtual-text").setup()

-- Use the same DAP configuration for C and Rust.
dap.configurations.c = dap.configurations.cpp
dap.configurations.rust = dap.configurations.cpp

-- Set up keybindings.
vim.api.nvim_set_keymap('n', '<leader>wc', "<Cmd>lua require'dap'.continue()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>wn', "<Cmd>lua require'dap'.step_over()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>ws', "<Cmd>lua require'dap'.step_into()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>wS', "<Cmd>lua require'dap'.step_out()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>wb', "<Cmd>lua require'dap'.toggle_breakpoint()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>wB', "<Cmd>lua require'dap'.set_breakpoint(vim.fn.input('Breakpoint condition: '))<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>wp', "<Cmd>lua require'dap'.set_breakpoint(nil, nil, vim.fn.input('Log point message: '))<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>wu', "<Cmd>lua require'dap'.up()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>wd', "<Cmd>lua require'dap'.down()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>wr', "<Cmd>lua require'dap'.repl.open()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>wl', "<Cmd>lua require'dap'.run_last()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>wt', "<Cmd>lua require'dap'.terminate()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>wg', "<Cmd>lua require'dapui'.toggle()<CR>", { noremap = true, silent = true })

-- dap-python
vim.api.nvim_set_keymap('n', '<leader>wC', "<Cmd>lua require'dap-python'.test_method({ config = { justMyCode = false } })<CR>", { noremap = true, silent = true })

-- Open virtual text diagnostics into a window.
vim.api.nvim_set_keymap('n', '<leader>of', "<Cmd>lua vim.diagnostic.open_float()<CR>", { noremap = true, silent = true })

require'nvim-treesitter.configs'.setup {
  ensure_installed = { "cpp", "c", "python" },
  highlight = {
    enable = true,              -- false will disable the whole extension
    additional_vim_regex_highlighting = false,
  },
  indent = {
    enable = true
  }
}
EOF
