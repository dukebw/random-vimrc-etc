# New Fedora Install Steps


- Enable RPM Fusion repositories (free and non-free) `https://docs.fedoraproject.org/en-US/quick-docs/setup_rpmfusion/`

- Install WiFi drivers (Broadcom BCM4360) `lspci -vnn | grep -i net`

- Install neovim (dnf)

- Set up Vundle `git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim`

- Copy neovim config from https://github.com/dukebw/random-vimrc-etc/.vimrc to `$HOME/.config/nvim/init.vim`

- Install Miniconda

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
. "$HOME/miniconda/etc/profile.d/conda.sh"
```

- `pip install neovim`

- Copy `.ssh/id_rsa*`, `.ssh/config`, `.ssh/brendan-laptop0.pem` from previous machine.

- Install CUDA and NVIDIA driver https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html

- Download Inconsolata and set fonts (gnome-tweaks)

- Setup dropbox (dnf)
