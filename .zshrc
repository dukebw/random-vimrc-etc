alias l="ls -alh"
source ~/miniconda/etc/profile.d/conda.sh
conda activate

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

export PATH=/usr/local/texlive/2022/bin/universal-darwin:$PATH

# The next line updates PATH for the Google Cloud SDK.
if [ -f '/Users/brendanduke/work/google-cloud-sdk/path.zsh.inc' ]; then . '/Users/brendanduke/work/google-cloud-sdk/path.zsh.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/Users/brendanduke/work/google-cloud-sdk/completion.zsh.inc' ]; then . '/Users/brendanduke/work/google-cloud-sdk/completion.zsh.inc'; fi

# NOTE(brendan): as of 2022/7/6, nodejs version 17 is needed for Copilot to
# work on Apple Silicon
nvm use 17

alias fdh='fdfind --hidden --no-ignore'
alias bc='clear-mojo-packages; rm -rf .derived/.{max,mojo}_cache; $MODULAR_PATH/.derived/autovenv/bin/python3 $MODULAR_PATH/utils/build.py build modular all max-mojo custom_rope_target'
alias ba='$MODULAR_PATH/.derived/autovenv/bin/python3 $MODULAR_PATH/utils/build.py build modular all max-mojo custom_rope_target'
source $MODULAR_DERIVED_PATH/autovenv/bin/activate
export PATH=$PATH:/usr/local/go/bin

# Set up fzf key bindings and fuzzy completion
source <(fzf --zsh)

# Fuzzy finder for Bazel.
# Source: https://blog.jez.io/fzf-bazel/
_fzf_complete_bazel_test() {
  _fzf_complete '-m' "$@" < <(command bazel query \
    "kind('(test|test_suite) rule', //...)" 2> /dev/null)
}

_fzf_complete_bazel() {
  local tokens
  tokens=(${(z)LBUFFER})

  if [ ${#tokens[@]} -ge 3 ] && [ "${tokens[2]}" = "test" ]; then
    _fzf_complete_bazel_test "$@"
  else
    # Might be able to make this better someday, by listing all repositories
    # that have been configured in a WORKSPACE.
    # See https://stackoverflow.com/questions/46229831/ or just run
    #     bazel query //external:all
    # This is the reason why things like @ruby_2_6//:ruby.tar.gz don't show up
    # in the output: they're not a dep of anything in //..., but they are deps
    # of @ruby_2_6//...
    _fzf_complete '-m' "$@" < <(command bazel query --keep_going \
      --noshow_progress \
      "kind('(binary rule)|(generated file)', deps(//...))" 2> /dev/null)
  fi
}
_fzf_complete_sb() { _fzf_complete_bazel "$@" }
_fzf_complete_sbg() { _fzf_complete_bazel "$@" }
_fzf_complete_sbgo() { _fzf_complete_bazel "$@" }
_fzf_complete_sbo() { _fzf_complete_bazel "$@" }
_fzf_complete_sbr() { _fzf_complete_bazel "$@" }
_fzf_complete_sbl() { _fzf_complete_bazel "$@" }
_fzf_complete_st() { _fzf_complete_bazel_test "$@" }
_fzf_complete_sto() { _fzf_complete_bazel_test "$@" }
_fzf_complete_stg() { _fzf_complete_bazel_test "$@" }
_fzf_complete_stog() { _fzf_complete_bazel_test "$@" }

alias bz-cc='bazelw run //:refresh_compile_commands -- --bazel ./bazelw'
