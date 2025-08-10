"""Create and configure MDCM instance."""

import base64
import os
import sys
from pathlib import Path

import click
import paramiko
from paramiko.proxy import ProxyCommand

# Define constants
remote_username = "ubuntu"
volume_name = "bduke-intel-500"
volume_size = 500
instance_type = "c5.12xlarge"
os_version = "22.04"

ZSHRC_EPILOGUE = r"""alias fdh="fdfind --hidden --no-ignore"
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

pyenv global 3.12

cd ~/work/modular
source utils/start-modular.sh

alias fdh='fdfind --hidden --no-ignore'
export PATH=$PATH:/usr/local/go/bin

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

export IBAZEL=/home/ubuntu/work/bazel-watcher/bazel-bin/cmd/ibazel/ibazel_/ibazel
alias bz-cc='bazelw run //:refresh_compile_commands -- --bazel ./bazelw && bash $HOME/work/random-vimrc-etc/fix_compile_commands.sh'
alias bz=$MODULAR_PATH/bazelw
export MODULAR_MOJO_MAX_COMPILERRT_PATH=$MODULAR_PATH/bazel-bin/KGEN/libKGENCompilerRTShared.so
export MODULAR_MOJO_MAX_IMPORT_PATH=$MODULAR_PATH/bazel-bin/Kernels/mojo/buffer,$MODULAR_PATH/bazel-bin/Kernels/mojo/register,$MODULAR_PATH/bazel-bin/SDK/integration-test,$MODULAR_PATH/bazel-bin/open-source/mojo/stdlib/stdlib

. "$HOME/.cargo/env"

# pnpm
export PNPM_HOME="/home/ubuntu/.local/share/pnpm"
case ":$PATH:" in
*":$PNPM_HOME:"*) ;;
*) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

alias ibb="$IBAZEL -bazel_path $MODULAR_PATH/bazelw build"
alias ibr="$IBAZEL -bazel_path $MODULAR_PATH/bazelw run"
alias ibt="$IBAZEL -bazel_path $MODULAR_PATH/bazelw test"

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# Put user-installed executables in PATH.
export PATH="$PATH:/home/ubuntu/.local/bin"
export EDITOR=nvim
source <(fzf --zsh)

export PIPELINES_TESTDATA=$MODULAR_PATH/SDK/integration-test/pipelines/python/llama3/testdata
export MODULAR_CUDA_QUERY_PATH=$MODULAR_PATH/bazel-bin/Kernels/tools/gpu-query/gpu-query

# Environment variables to convince pylsp_mypy to work as expected with Bazel.
export MAX_PYTHON_VENV=$MODULAR_PATH/.SDK+lib+API+python+max+entrypoints+pipelines.venv
# This is used in my Neovim config.
export PYLSP_VENV_PATH=$MAX_PYTHON_VENV
export PYLSP_MYPY_CONFIG=$HOME/work/modular/mypy.ini
export MYPYPATH=$MODULAR_PATH/bazel-bin/SDK/lib/API/python/max/entrypoints/pipelines.runfiles/_main/SDK/lib/API/python
source $MAX_PYTHON_VENV/bin/activate

# Allow debugging to attach to process, and profiling.
sudo sysctl -w kernel.yama.ptrace_scope=0
export HF_TOKEN=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

# Add additional environment variables.
[ -f ~/.env ] && source ~/.env
        """


def run_ssh_command(ssh_client, command, timeout=None):
    chan = ssh_client.get_transport().open_session()
    chan.settimeout(timeout or 60)
    chan.exec_command(command)

    stdout = chan.makefile("r")
    stderr = chan.makefile_stderr("r")

    # Stream both pipes without mis-labelling normal progress text.
    for line in iter(stdout.readline, ""):
        print(line, end="")

    for line in iter(stderr.readline, ""):
        # print to console but don't assume failure.
        print(line, end="", file=sys.stderr)

    exit_status = chan.recv_exit_status()
    if exit_status != 0:
        # Intentionally continue.
        print(f"{command!r} failed with exit = {exit_status}")


@click.group()
def cli():
    """CLI commands."""


@cli.command()
@click.option("--vm-ip", type=str, required=True, help="IP address of the VM")
@click.option(
    "--vm-name", type=str, default="c6i.16xlarge", help="Name of the VM"
)
def install_configure(vm_ip: str, vm_name: str):
    """SSH into the VM and run install and configuration commands."""
    remote_work_dir = "~/work"
    gcl = "GIT_SSH_COMMAND='ssh -o StrictHostKeyChecking=no' git clone --recurse-submodules"

    # Same command as in your ~/.ssh/config
    proxy_cmd = f'/usr/local/bin/coder --global-config "/Users/bduke/Library/Application Support/coderv2" ssh --stdio {vm_name}'
    # proxy_cmd = "ssh -i ~/.ssh/mdcm.pem -o StrictHostKeyChecking=no -W 10.250.102.186:22 ubuntu@10.250.102.186"

    with ProxyCommand(proxy_cmd) as proxy_socket:
        transport = paramiko.Transport(proxy_socket)
        transport.start_client()
        # Attempt none authentication explicitly
        transport.auth_none(remote_username)
        # private_key = paramiko.Ed25519Key.from_private_key_file(
        #     Path("~/.ssh/mdcm.pem").expanduser()
        # )
        # transport.connect(username=remote_username, pkey=private_key)
        # transport.connect(username=remote_username)

        # If we get here, 'none' authentication worked.
        ssh_client = paramiko.SSHClient()
        ssh_client._transport = transport
        # Now you can execute commands as usual:
        stdin, stdout, stderr = ssh_client.exec_command("ls")
        print(stdout.read().decode("utf-8"))

        # Ensure .ssh directory exists on remote.
        run_ssh_command(ssh_client, "mkdir -p ~/.ssh && chmod 700 ~/.ssh")

        # Upload local SSH key to the remote instance.
        with ssh_client.open_sftp() as sftp_client:
            local_ssh_key = Path("~/.ssh/id_ed25519").expanduser()
            if local_ssh_key.exists():
                remote_key_path = ".ssh/id_ed25519"
                sftp_client.put(str(local_ssh_key), remote_key_path)
                sftp_client.chmod(remote_key_path, 0o600)  # Required by SSH

        # Create SFTP client for file transfers.
        with ssh_client.open_sftp() as sftp_client:
            if (env_path := Path.home() / ".env").exists():
                # Copy the env variables, which the `ZSHRC_EPILOGUE` sources.
                sftp_client.put(str(env_path), ".env")
                sftp_client.chmod(".env", 0o600)

        # Set up locale.
        run_ssh_command(
            ssh_client,
            "sudo sed -i 's/# en_CA.UTF-8 UTF-8/en_CA.UTF-8 UTF-8/' /etc/locale.gen",
        )
        run_ssh_command(ssh_client, "sudo locale-gen")
        run_ssh_command(ssh_client, "sudo update-locale LANG=en_CA.UTF-8")

        # Non-interactive apt upgrade.
        apt = "DEBIAN_FRONTEND=noninteractive apt-get"

        # Update and install oh-my-zsh
        run_ssh_command(
            ssh_client,
            f"sudo {apt} update && sudo {apt} -y upgrade",
        )
        run_ssh_command(
            ssh_client,
            f"sudo {apt} install -y expect xclip zsh protobuf-compiler fd-find pipx less git-lfs make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev",
        )
        run_ssh_command(ssh_client, "pipx install stack-pr")
        run_ssh_command(ssh_client, "sudo passwd -d `whoami`")
        run_ssh_command(ssh_client, "sudo chsh -s $(which zsh)")
        run_ssh_command(
            ssh_client,
            (
                "curl -fsSL"
                " https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
                " -o install_oh_my_zsh.sh"
            ),
        )
        run_ssh_command(ssh_client, "chmod +x install_oh_my_zsh.sh")

        expect_script = (
            "#!/usr/bin/expect\n"
            "set timeout 5\n"
            'spawn sh -c "./install_oh_my_zsh.sh"\n'
            'expect "Do you want to change your default shell to zsh?"\n'
            'send "y\\r"\n'
            "expect eof\n"
        )
        # Creating the Expect script on the remote machine
        run_ssh_command(
            ssh_client, f"echo -e '{expect_script}' > install_oh_my_zsh.expect"
        )
        run_ssh_command(ssh_client, "chmod +x install_oh_my_zsh.expect")
        run_ssh_command(
            ssh_client, "rm -rf ~/.oh-my-zsh && ./install_oh_my_zsh.expect"
        )

        # TODO: this should be in install-dependencies.py
        run_ssh_command(ssh_client, f"sudo {apt} install -y libtbb-dev")
        run_ssh_command(
            ssh_client,
            f"sudo {apt} install -y ~/NsightSystems-linux-cli-public-2024.7.1.84-3512561.deb",
        )

        # Install neovim.
        run_ssh_command(
            ssh_client,
            (
                "curl -fsSL"
                " https://github.com/neovim/neovim/releases/download/v0.11.3/nvim-linux-x86_64.tar.gz"
                " -o nvim-linux-x86_64.tar.gz"
            ),
        )
        run_ssh_command(ssh_client, "tar zxf nvim-linux-x86_64.tar.gz")
        run_ssh_command(
            ssh_client,
            "sudo ln -s $(pwd)/nvim-linux-x86_64/bin/nvim /usr/local/bin",
        )

        run_ssh_command(
            ssh_client,
            (
                f"mkdir -p ~/work && {gcl} git@github.com:dukebw/random-vimrc-etc"
                " ~/work/random-vimrc-etc"
            ),
        )

        # Configure neovim.
        run_ssh_command(
            ssh_client,
            f'{gcl} git@github.com:dukebw/kickstart.nvim.git "${{XDG_CONFIG_HOME:-$HOME/.config}}"/nvim',
        )

        # Perform final setup
        run_ssh_command(
            ssh_client,
            (
                f"cd {remote_work_dir} && {gcl} git@github.com:modularml/modular && cd"
                " modular && source utils/start-modular.sh && install_python_deps &&"
                " install_dev_deps"
            ),
        )
        # Setup vim syntax highlighting for MLIR, LLVM, and Mojo
        # First, trigger LLVM download by running a simple bazel query
        run_ssh_command(
            ssh_client,
            f"cd {remote_work_dir}/modular && ./bazelw query @llvm-project//... --keep_going --noshow_progress 2>/dev/null || true",
        )

        # Setup MLIR syntax highlighting
        run_ssh_command(
            ssh_client,
            (
                f"cd {remote_work_dir}/modular && "
                "LLVM_PATH=bazel-modular/external/+http_archive+llvm-raw && "
                "if [ -d $LLVM_PATH/mlir/utils/vim ]; then "
                "  for FOLDER in ftdetect ftplugin indent syntax; do "
                "    mkdir -p ~/.config/nvim/$FOLDER && "
                "    [ -f $LLVM_PATH/mlir/utils/vim/$FOLDER/mlir.vim ] && "
                "    ln -sf $(pwd)/$LLVM_PATH/mlir/utils/vim/$FOLDER/mlir.vim ~/.config/nvim/$FOLDER/mlir.vim; "
                "  done; "
                "fi"
            ),
        )

        # Setup LLVM syntax highlighting (tablegen, llvm, llvm-lit, mir)
        for filetype in ["tablegen", "llvm", "llvm-lit", "mir"]:
            run_ssh_command(
                ssh_client,
                (
                    f"cd {remote_work_dir}/modular && "
                    "LLVM_PATH=bazel-modular/external/+http_archive+llvm-raw && "
                    "if [ -d $LLVM_PATH/llvm/utils/vim ]; then "
                    "  for FOLDER in ftdetect ftplugin indent syntax; do "
                    "    mkdir -p ~/.config/nvim/$FOLDER && "
                    f"    [ -f $LLVM_PATH/llvm/utils/vim/$FOLDER/{filetype}.vim ] && "
                    f"    ln -sf $(pwd)/$LLVM_PATH/llvm/utils/vim/$FOLDER/{filetype}.vim ~/.config/nvim/$FOLDER/{filetype}.vim; "
                    "  done; "
                    "fi"
                ),
            )

        # Setup Mojo syntax highlighting
        run_ssh_command(
            ssh_client,
            (
                f"cd {remote_work_dir}/modular && "
                "for FOLDER in autoload ftdetect ftplugin indent syntax; do "
                "  mkdir -p ~/.config/nvim/$FOLDER && "
                "  [ -f utils/mojo/vim/$FOLDER/mojo.vim ] && "
                "  ln -sf $(pwd)/utils/mojo/vim/$FOLDER/mojo.vim ~/.config/nvim/$FOLDER/mojo.vim; "
                "done"
            ),
        )

        run_ssh_command(
            ssh_client,
            "cp ~/work/random-vimrc-etc/local.bazelrc ~/work/modular",
        )

        # Copy nvim-dap.json over to modular repo.
        run_ssh_command(
            ssh_client,
            f"cp ~/work/random-vimrc-etc/.nvim-dap.json {remote_work_dir}/modular",
        )

        # TODO: LLVM 16 works on c7g, but not LLVM 18.
        if "c7g" not in vm_name:
            run_ssh_command(
                ssh_client,
                ('sudo bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"'),
            )
        run_ssh_command(
            ssh_client,
            (
                "sudo update-alternatives --install /usr/bin/cc cc /usr/bin/clang 100 && "
                "sudo update-alternatives --install /usr/bin/c++ c++ /usr/bin/clang++ 100"
            ),
        )

        run_ssh_command(
            ssh_client,
            (
                "git config --global user.name 'Brendan Duke' && git config --global user.email 'bduke@modular.com'"
            ),
        )

        run_ssh_command(
            ssh_client,
            ("sed -i 's/plugins=(git)/plugins=(git vi-mode)/' ~/.zshrc"),
        )

        # Encode the .zshrc epilogue to base64 to avoid issues with special
        # characters on the command line.
        zshrc_epilogue_quoted = base64.b64encode(
            ZSHRC_EPILOGUE.encode("utf-8")
        ).decode("utf-8")
        run_ssh_command(
            ssh_client,
            f'echo "{zshrc_epilogue_quoted}" | base64 --decode >> ~/.zshrc',
        )

        # Install pyenv.
        run_ssh_command(
            ssh_client, "curl https://pyenv.run | bash && pyenv install 3.12"
        )

        # Install latest LLVM.
        run_ssh_command(
            ssh_client, "cd ~/work/modular && ./utils/install-llvm.sh"
        )

        # Install pnpm.
        run_ssh_command(
            ssh_client, "curl -fsSL https://get.pnpm.io/install.sh | sh -"
        )

        # Install nvm.
        run_ssh_command(
            ssh_client,
            "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash",
        )

        # Install node.
        run_ssh_command(ssh_client, "nvm install node && nvm use node")

        # Install bazelrc-lsp.
        run_ssh_command(
            ssh_client,
            (
                f"cd ~/work && {gcl} git@github.com:salesforce-misc/bazelrc-lsp && cd bazelrc-lsp/vscode-extension && pnpm i && pnpm package"
            ),
        )

        # Install bazel-lsp.
        run_ssh_command(
            ssh_client,
            f"cd ~/work && {gcl} git@github.com:cameron-martin/bazel-lsp && cd bazel-lsp && bazel build //:bazel-lsp -c opt",
        )

        # Install ibazel.
        run_ssh_command(
            ssh_client,
            f"cd ~/work && {gcl} git@github.com:bazelbuild/bazel-watcher && cd bazel-watcher && bazel build //cmd/ibazel",
        )

        # Make local directory to install executables.
        run_ssh_command(ssh_client, "mkdir -p ~/.local/bin")

        # Copy codex-tmux and tmux-codex.conf files.
        with ssh_client.open_sftp() as sftp_client:
            # Copy codex-tmux script.
            local_codex_tmux = Path(__file__).parent / "files" / "codex-tmux"
            if local_codex_tmux.exists():
                remote_codex_tmux = ".local/bin/codex-tmux"
                sftp_client.put(str(local_codex_tmux), remote_codex_tmux)
                sftp_client.chmod(remote_codex_tmux, 0o755)  # Make executable

            # Copy tmux-codex.conf.
            local_tmux_conf = (
                Path(__file__).parent / "files" / "tmux-codex.conf"
            )
            if local_tmux_conf.exists():
                remote_tmux_conf = ".local/bin/tmux-codex.conf"
                sftp_client.put(str(local_tmux_conf), remote_tmux_conf)
                sftp_client.chmod(remote_tmux_conf, 0o644)

            # Copy codex-init-session script.
            local_codex_init = (
                Path(__file__).parent / "files" / "codex-init-session"
            )
            if local_codex_init.exists():
                remote_codex_init = ".local/bin/codex-init-session"
                sftp_client.put(str(local_codex_init), remote_codex_init)
                sftp_client.chmod(remote_codex_init, 0o755)  # Make executable

            # Create ~/.codex directory and copy configuration files.
            run_ssh_command(ssh_client, "mkdir -p ~/.codex")

            # Copy AGENTS.md from files directory.
            local_agents_md = Path(__file__).parent / "files" / "AGENTS.md"
            if local_agents_md.exists():
                remote_agents_md = ".codex/AGENTS.md"
                sftp_client.put(str(local_agents_md), remote_agents_md)
                sftp_client.chmod(remote_agents_md, 0o644)

            # Copy config.toml from files directory.
            local_config_toml = Path(__file__).parent / "files" / "config.toml"
            if local_config_toml.exists():
                remote_config_toml = ".codex/config.toml"
                sftp_client.put(str(local_config_toml), remote_config_toml)
                sftp_client.chmod(remote_config_toml, 0o644)

        # Install delta.
        run_ssh_command(
            ssh_client,
            "cd ~/work && curl -fSsL https://github.com/dandavison/delta/releases/download/0.18.2/delta-0.18.2-x86_64-unknown-linux-gnu.tar.gz -o delta-0.18.2-x86_64-unknown-linux-gnu.tar.gz && tar zxvf delta-0.18.2-x86_64-unknown-linux-gnu.tar.gz && ln -s $(pwd)/delta-0.18.2-x86_64-unknown-linux-gnu/delta ~/.local/bin",
        )

        print("Installation and configuration completed.")

        # Set .gitconfig.
        gitconfig = r"""
[blame]
  pager = delta

[core]
	editor = nvim -u ~/.config/nvim/init.lua
  pager = delta

[delta]
  features = calochortus-lyallii side-by-side
  line-numbers = false
  hyperlinks = true
  navigate = true    # use n and N to move between diff sections
  light = false      # set to true if you're in a terminal w/ a light background color (e.g. the default macOS terminal)

[diff]
  colorMoved = default

[filter "lfs"]
	required = true
	clean = git-lfs clean -- %f
	smudge = git-lfs smudge -- %f
	process = git-lfs filter-process

[include]
  path = ~/work/delta/themes.gitconfig

[interactive]
  diffFilter = delta --color-only

[merge]
  conflictstyle = diff3

[pull]
	rebase = false

[user]
	name = Brendan Duke
	email = brendanw.duke@gmail.com
[maintenance]
	repo = /home/ubuntu/work/modular
"""
        gittconfig_quoted = base64.b64encode(gitconfig.encode("utf-8")).decode(
            "utf-8"
        )
        run_ssh_command(
            ssh_client,
            f'echo "{gittconfig_quoted}" | base64 --decode > ~/.gitconfig',
        )

        # Install cargo.
        run_ssh_command(
            ssh_client,
            "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y",
        )

        # Install Tokei, the line of code counter.
        run_ssh_command(ssh_client, "cargo install tokei")

        # Install tree-sitter CLI, needed for MLIR.
        run_ssh_command(ssh_client, "cargo install --locked tree-sitter-cli")

        # Set up python dependencies.
        # nvim-dap-python needs debugpy.
        run_ssh_command(
            ssh_client, "pip install --upgrade pip debugpy pynvim nvitop"
        )

        # Install fzf.
        run_ssh_command(
            ssh_client,
            "git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf && ~/.fzf/install --all --no-bash --no-fish",
        )

        run_ssh_command(
            ssh_client,
            "sudo mkdir -p /usr/local/cuda/lib64 && sudo ln -s /usr/local/cuda-12.6/targets/x86_64-linux/lib/libnvToolsExt.so /usr/local/cuda/lib64/libnvToolsExt.so",
        )

        os.system(f"ssh -Y coder.{vm_name}")

        # Close the SSH connection.
        ssh_client.close()


@cli.command()
@click.option(
    "--vm-name", type=str, default="bduke-a100", help="Name of the VM"
)
def coder(vm_name: str) -> None:
    """SSH into the VM and run install and configuration commands."""
    gcl = "git clone --recurse-submodules"

    # Same command as in your ~/.ssh/config
    proxy_cmd = f'/usr/local/bin/coder --global-config "/Users/bduke/Library/Application Support/coderv2" ssh --stdio {vm_name}'

    with ProxyCommand(proxy_cmd) as proxy_socket:
        transport = paramiko.Transport(proxy_socket)
        transport.start_client()
        # Attempt none authentication explicitly.
        transport.auth_none(remote_username)

        # If we get here, 'none' authentication worked.
        ssh_client = paramiko.SSHClient()
        ssh_client._transport = transport
        # Now you can execute commands as usual:
        stdin, stdout, stderr = ssh_client.exec_command("ls")
        print(stdout.read().decode("utf-8"))

        # Create SFTP client for file transfers.
        with ssh_client.open_sftp() as sftp_client:
            if (env_path := Path.home() / ".env").exists():
                # Copy the env variables, which the `ZSHRC_EPILOGUE` sources.
                sftp_client.put(str(env_path), ".env")
                sftp_client.chmod(".env", 0o600)

        # Set up locale.
        run_ssh_command(
            ssh_client,
            "sudo sed -i 's/# en_CA.UTF-8 UTF-8/en_CA.UTF-8 UTF-8/' /etc/locale.gen",
        )
        run_ssh_command(ssh_client, "sudo locale-gen")
        run_ssh_command(ssh_client, "sudo update-locale LANG=en_CA.UTF-8")

        # Non-interactive apt upgrade.
        apt = "DEBIAN_FRONTEND=noninteractive apt-get"
        run_ssh_command(
            ssh_client,
            f"sudo {apt} update && sudo {apt} -y upgrade",
        )
        run_ssh_command(
            ssh_client,
            f"sudo {apt} install -y expect xclip zsh protobuf-compiler fd-find pipx less",
        )
        run_ssh_command(ssh_client, "pipx install stack-pr")
        run_ssh_command(ssh_client, "sudo passwd -d `whoami`")
        run_ssh_command(ssh_client, "sudo chsh -s $(which zsh)")
        run_ssh_command(
            ssh_client,
            (
                "curl -fsSL"
                " https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
                " -o install_oh_my_zsh.sh"
            ),
        )
        run_ssh_command(ssh_client, "chmod +x install_oh_my_zsh.sh")

        expect_script = (
            "#!/usr/bin/expect\n"
            "set timeout 5\n"
            'spawn sh -c "./install_oh_my_zsh.sh"\n'
            'expect "Do you want to change your default shell to zsh?"\n'
            'send "y\\r"\n'
            "expect eof\n"
        )
        # Creating the Expect script on the remote machine
        run_ssh_command(
            ssh_client,
            f"echo -e '{expect_script}' > install_oh_my_zsh.expect",
        )
        run_ssh_command(ssh_client, "chmod +x install_oh_my_zsh.expect")
        run_ssh_command(
            ssh_client, "rm -rf ~/.oh-my-zsh && ./install_oh_my_zsh.expect"
        )

        # TODO: this should be in install-dependencies.py
        run_ssh_command(ssh_client, f"sudo {apt} install -y libtbb-dev")
        # run_ssh_command(
        #     ssh_client,
        #     f"sudo {apt} install -y ~/NsightSystems-linux-cli-public-2024.7.1.84-3512561.deb",
        # )

        # Install neovim.
        run_ssh_command(
            ssh_client,
            (
                "curl -fsSL"
                " https://github.com/neovim/neovim/releases/download/v0.11.3/nvim-linux-x86_64.tar.gz"
                " -o nvim-linux-x86_64.tar.gz"
            ),
        )
        run_ssh_command(ssh_client, "tar zxf nvim-linux-x86_64.tar.gz")
        run_ssh_command(
            ssh_client,
            "sudo ln -s $(pwd)/nvim-linux-x86_64/bin/nvim /usr/local/bin",
        )

        run_ssh_command(
            ssh_client,
            (
                f"mkdir -p ~/work && {gcl} git@github.com:dukebw/random-vimrc-etc"
                " ~/work/random-vimrc-etc"
            ),
        )

        # Configure neovim.
        run_ssh_command(
            ssh_client,
            f'{gcl} git@github.com:dukebw/kickstart.nvim.git "${{XDG_CONFIG_HOME:-$HOME/.config}}"/nvim',
        )

        run_ssh_command(
            ssh_client,
            (
                "sudo update-alternatives --install /usr/bin/cc cc /usr/bin/clang 100 && "
                "sudo update-alternatives --install /usr/bin/c++ c++ /usr/bin/clang++ 100"
            ),
        )

        run_ssh_command(
            ssh_client,
            (
                "git config --global user.name 'Brendan Duke' && git config --global user.email 'bduke@modular.com'"
            ),
        )

        run_ssh_command(
            ssh_client,
            ("sed -i 's/plugins=(git)/plugins=(git vi-mode)/' ~/.zshrc"),
        )

        # Encode the .zshrc epilogue to base64 to avoid issues with special
        # characters on the command line.
        zshrc_epilogue_quoted = base64.b64encode(
            ZSHRC_EPILOGUE.encode("utf-8")
        ).decode("utf-8")
        run_ssh_command(
            ssh_client,
            f'echo "{zshrc_epilogue_quoted}" | base64 --decode >> ~/.zshrc',
        )

        # Install pyenv.
        run_ssh_command(
            ssh_client,
            "curl https://pyenv.run | bash && pyenv install 3.12",
        )

        # Install latest LLVM.
        run_ssh_command(
            ssh_client, "cd ~/work/modular && ./utils/install-llvm.sh"
        )

        # Install pnpm.
        run_ssh_command(
            ssh_client, "curl -fsSL https://get.pnpm.io/install.sh | sh -"
        )

        # Install nvm.
        run_ssh_command(
            ssh_client,
            "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash",
        )

        # Install node.
        run_ssh_command(ssh_client, "nvm install node && nvm use node")

        # Install bazelrc-lsp.
        run_ssh_command(
            ssh_client,
            (
                f"cd ~/work && {gcl} git@github.com:salesforce-misc/bazelrc-lsp && cd bazelrc-lsp/vscode-extension && pnpm i && pnpm package"
            ),
        )

        # Install bazel-lsp.
        run_ssh_command(
            ssh_client,
            f"cd ~/work && {gcl} git@github.com:cameron-martin/bazel-lsp && cd bazel-lsp && bazel build //:bazel-lsp -c opt",
        )

        # Install ibazel.
        run_ssh_command(
            ssh_client,
            f"cd ~/work && {gcl} git@github.com:bazelbuild/bazel-watcher && cd bazel-watcher && bazel build //cmd/ibazel",
        )

        # Make local directory to install executables.
        run_ssh_command(ssh_client, "mkdir -p ~/.local/bin")

        # Copy codex-tmux, claude-tmux and tmux-codex.conf files
        with ssh_client.open_sftp() as sftp_client:
            # Copy codex-tmux script
            local_codex_tmux = Path(__file__).parent / "files" / "codex-tmux"
            if local_codex_tmux.exists():
                remote_codex_tmux = ".local/bin/codex-tmux"
                sftp_client.put(str(local_codex_tmux), remote_codex_tmux)
                sftp_client.chmod(remote_codex_tmux, 0o755)  # Make executable

            # Copy claude-tmux script
            local_claude_tmux = Path(__file__).parent / "files" / "claude-tmux"
            if local_claude_tmux.exists():
                remote_claude_tmux = ".local/bin/claude-tmux"
                sftp_client.put(str(local_claude_tmux), remote_claude_tmux)
                sftp_client.chmod(remote_claude_tmux, 0o755)  # Make executable

            # Copy tmux-codex.conf
            local_tmux_conf = (
                Path(__file__).parent / "files" / "tmux-codex.conf"
            )
            if local_tmux_conf.exists():
                remote_tmux_conf = ".local/bin/tmux-codex.conf"
                sftp_client.put(str(local_tmux_conf), remote_tmux_conf)
                sftp_client.chmod(remote_tmux_conf, 0o644)

            # Copy codex-init-session script
            local_codex_init = (
                Path(__file__).parent / "files" / "codex-init-session"
            )
            if local_codex_init.exists():
                remote_codex_init = ".local/bin/codex-init-session"
                sftp_client.put(str(local_codex_init), remote_codex_init)
                sftp_client.chmod(remote_codex_init, 0o755)  # Make executable

            # Create ~/.codex directory and copy configuration files
            run_ssh_command(ssh_client, "mkdir -p ~/.codex")

            # Copy AGENTS.md from files directory
            local_agents_md = Path(__file__).parent / "files" / "AGENTS.md"
            if local_agents_md.exists():
                remote_agents_md = ".codex/AGENTS.md"
                sftp_client.put(str(local_agents_md), remote_agents_md)
                sftp_client.chmod(remote_agents_md, 0o644)

            # Copy config.toml from files directory
            local_config_toml = Path(__file__).parent / "files" / "config.toml"
            if local_config_toml.exists():
                remote_config_toml = ".codex/config.toml"
                sftp_client.put(str(local_config_toml), remote_config_toml)
                sftp_client.chmod(remote_config_toml, 0o644)

        # Install delta.
        run_ssh_command(
            ssh_client,
            "cd ~/work && curl -fSsL https://github.com/dandavison/delta/releases/download/0.18.2/delta-0.18.2-x86_64-unknown-linux-gnu.tar.gz -o delta-0.18.2-x86_64-unknown-linux-gnu.tar.gz && tar zxvf delta-0.18.2-x86_64-unknown-linux-gnu.tar.gz && ln -s $(pwd)/delta-0.18.2-x86_64-unknown-linux-gnu/delta ~/.local/bin",
        )

        print("Installation and configuration completed.")

        # Set .gitconfig.
        gitconfig = r"""
[blame]
  pager = delta

[core]
        editor = nvim -u ~/.config/nvim/init.lua
  pager = delta

[delta]
  features = calochortus-lyallii side-by-side
  line-numbers = false
  hyperlinks = true
  navigate = true    # use n and N to move between diff sections
  light = false      # set to true if you're in a terminal w/ a light background color (e.g. the default macOS terminal)

[diff]
  colorMoved = default

[filter "lfs"]
        required = true
        clean = git-lfs clean -- %f
        smudge = git-lfs smudge -- %f
        process = git-lfs filter-process

[include]
  path = ~/work/delta/themes.gitconfig

[interactive]
  diffFilter = delta --color-only

[merge]
  conflictstyle = diff3

[pull]
        rebase = false

[user]
        name = Brendan Duke
        email = brendanw.duke@gmail.com
[maintenance]
        repo = /home/ubuntu/work/modular
"""
        gittconfig_quoted = base64.b64encode(gitconfig.encode("utf-8")).decode(
            "utf-8"
        )
        run_ssh_command(
            ssh_client,
            f'echo "{gittconfig_quoted}" | base64 --decode > ~/.gitconfig',
        )

        run_ssh_command(
            ssh_client,
            "cd ~/work/modular && source utils/start-modular.sh && install_dev_deps",
        )

        # Install cargo.
        run_ssh_command(
            ssh_client,
            "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y",
        )

        # Install Tokei, the line of code counter.
        run_ssh_command(ssh_client, "cargo install tokei")

        # Install tree-sitter CLI, needed for MLIR.
        run_ssh_command(ssh_client, "cargo install --locked tree-sitter-cli")

        # Set up python dependencies.
        # nvim-dap-python needs debugpy.
        run_ssh_command(
            ssh_client, "pip install --upgrade pip debugpy pynvim nvitop"
        )

        # Install fzf.
        run_ssh_command(
            ssh_client,
            "git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf && ~/.fzf/install --all --no-bash --no-zsh --no-fish --no-update-rc",
        )

        run_ssh_command(
            ssh_client,
            "sudo mkdir -p /usr/local/cuda/lib64 && sudo ln -s /usr/local/cuda-12.6/targets/x86_64-linux/lib/libnvToolsExt.so /usr/local/cuda/lib64/libnvToolsExt.so",
        )

        os.system(f"ssh -Y coder.{vm_name}")

        # Close the SSH connection.
        ssh_client.close()


if __name__ == "__main__":
    cli()
