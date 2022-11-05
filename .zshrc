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
