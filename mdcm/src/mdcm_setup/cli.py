"""Create and configure MDCM instance."""

import base64
import os
import shlex
import socket
import subprocess
from pathlib import Path

import click
import paramiko

# Define constants
remote_username = "ubuntu"
volume_name = "bduke-intel-500"
volume_size = 500
instance_type = "c5.12xlarge"
os_version = "22.04"

# Function to run local commands


def run_local_command(command):
    print(command)
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Local command error: {stderr}")
        exit(1)

    print(stdout.decode())
    return stdout


# Function to execute remote commands via SSH


def run_ssh_command(ssh_client, command, timeout=None):
    print(command)
    try:
        _, stdout, stderr = ssh_client.exec_command(command, timeout=timeout)

        # Continuously read and print stdout
        for line in iter(stdout.readline, ""):
            print(line, end="")

        # Check for any errors
        error_output = stderr.read().decode()
        if error_output:
            print(f"SSH command error: {error_output}")

            stdout.channel.recv_exit_status()
    except socket.timeout:
        print("Command timed out.")


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--vm-name", type=str, default="c6i.16xlarge", help="Name of the VM"
)
def create_vm(vm_name: str):
    """Create and start the VM."""
    run_local_command(
        f"mdcm volume create --name {volume_name} --size {volume_size}"
    )
    run_local_command(
        f"mdcm vm create -n {vm_name} -t {instance_type} -osver {os_version} -v"
        f" {volume_name}"
    )
    run_local_command(f"mdcm vm start --name {vm_name}")
    print(f"VM {vm_name} created and started.")


@cli.command()
@click.option("--vm-ip", type=str, required=True, help="IP address of the VM")
@click.option(
    "--vm-name", type=str, default="c6i.16xlarge", help="Name of the VM"
)
def install_configure(vm_ip: str, vm_name: str):
    """SSH into the VM and run install and configuration commands."""
    local_home_dir = Path(os.getenv("HOME"))
    key_path = local_home_dir / ".ssh" / "mdcm.pem"
    remote_work_dir = "~/work"

    # SSH into the VM
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(
        vm_ip, username=remote_username, key_filename=str(key_path)
    )

    # Update and install oh-my-zsh
    run_ssh_command(ssh_client, "sudo apt update && sudo apt upgrade -y")
    run_ssh_command(
        ssh_client,
        "sudo apt install -y expect xclip zsh protobuf-compiler fd-find",
    )
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
    run_ssh_command(ssh_client, "./install_oh_my_zsh.expect")

    # Copy SSH keys to VM
    run_local_command(
        f"scp -o 'StrictHostKeyChecking=no' -i {str(key_path)} ~/.ssh/id_ed25519*"
        f" {remote_username}@{vm_ip}:.ssh"
    )

    # Install neovim
    is_graviton = ("c6g" in vm_name) or ("c7g" in vm_name)
    if is_graviton:
        # Install neovim from source.
        run_ssh_command(
            ssh_client,
            "sudo apt install -y ninja-build gettext cmake unzip curl fd-find",
        )
        run_ssh_command(
            ssh_client,
            (
                "curl -fsSL"
                " https://github.com/neovim/neovim/archive/refs/tags/v0.10.1.tar.gz -o"
                " nvim-v0.10.1.tar.gz && tar zxf nvim-v0.10.1.tar.gz && cd neovim-0.10.1"
                " && make CMAKE_BUILD_TYPE=Release && sudo make install"
            ),
        )
    else:
        # TODO: this should be in install-dependencies.py
        run_ssh_command(ssh_client, "sudo apt install -y libtbb-dev")
        run_ssh_command(
            ssh_client,
            (
                "curl -fsSL"
                " https://github.com/neovim/neovim/releases/download/v0.10.1/nvim-linux64.tar.gz"
                " -o nvim-linux64.tar.gz"
            ),
        )
        run_ssh_command(ssh_client, "tar zxf nvim-linux64.tar.gz")
        run_ssh_command(
            ssh_client, "sudo ln -s $(pwd)/nvim-linux64/bin/nvim /usr/local/bin"
        )

    # Configure neovim
    gcl = (
        "GIT_SSH_COMMAND='ssh -o StrictHostKeyChecking=no' git clone"
        " --recurse-submodules"
    )
    run_ssh_command(
        ssh_client,
        (
            f"mkdir -p ~/work && {gcl} git@github.com:dukebw/random-vimrc-etc"
            " ~/work/random-vimrc-etc"
        ),
    )
    run_ssh_command(
        ssh_client,
        "mkdir -p ~/.config/nvim && cp ~/work/random-vimrc-etc/init.vim ~/.config/nvim",
    )

    # Install vim-plug
    run_ssh_command(
        ssh_client,
        (
            "sh -c 'curl -fLo"
            ' "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim'
            " --create-dirs"
            " https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'"
        ),
    )
    # Set a timeout since this seems to hang.
    run_ssh_command(
        ssh_client,
        "nvim -c 'PlugUpgrade | PlugInstall | PlugUpdate | qa!'",
        timeout=30,
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
    run_ssh_command(
        ssh_client,
        (
            f"cd {remote_work_dir}/modular/third-party/llvm-project/mlir && for FOLDER in"
            " ftdetect ftplugin indent syntax; do mkdir -p ~/.config/nvim/$FOLDER &&"
            " ln -s $(pwd)/utils/vim/$FOLDER/mlir.vim ~/.config/nvim/$FOLDER/mlir.vim;"
            " done"
        ),
    )
    for filetype in ["tablegen", "llvm", "llvm-lit", "mir"]:
        run_ssh_command(
            ssh_client,
            (
                f"cd {remote_work_dir}/modular/third-party/llvm-project/llvm && for FOLDER in"
                " ftdetect ftplugin indent syntax; do mkdir -p ~/.config/nvim/$FOLDER &&"
                f" ln -s $(pwd)/utils/vim/$FOLDER/{filetype}.vim ~/.config/nvim/$FOLDER/{filetype}.vim;"
                " done"
            ),
        )
    run_ssh_command(
        ssh_client,
        (
            f"cd {remote_work_dir}/modular && for FOLDER in autoload ftdetect"
            " ftplugin indent syntax; do mkdir -p ~/.config/nvim/$FOLDER && ln -s"
            " $(pwd)/utils/mojo/vim/$FOLDER/mojo.vim ~/.config/nvim/$FOLDER/mojo.vim;"
            " done"
        ),
    )

    # TODO: LLVM 16 works on c7g, but not LLVM 18.
    if not ("c7g" in vm_name):
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
    zshrc_epilogue = base64.b64encode(r"""alias fdh="fdfind --hidden --no-ignore"
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

pyenv global 3.12

cd ~/work/modular
source utils/start-modular.sh

alias fdh='fdfind --hidden --no-ignore'
source $MODULAR_DERIVED_PATH/autovenv/bin/activate
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
export PYTHONPATH=$MODULAR_PATH/bazel-bin/SDK/lib/API/python:$MODULAR_PATH/SDK/lib/API/python:$MODULAR_PATH/SDK/public/max-repo/pipelines/python
export MYPYPATH=$PYTHONPATH
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
export BAZEL_AWS_ECR_PASSWORD=$(aws ecr get-login-password --region us-east-1)

# Put user-installed executables in PATH.
export PATH="$PATH:/home/ubuntu/.local/bin"
""")
    run_ssh_command(
        ssh_client,
        f'echo "{shlex.quote(zshrc_epilogue)}" | base64 --decode >> ~/.zshrc',
    )

    # Install pyenv.
    run_ssh_command(
        ssh_client, "curl https://pyenv.run | bash && pyenv install 3.12"
    )

    local_bazlerc = r"""# Build all code with -O3, -gline-tables-only, and -fno-omit-frame-pointer.
# Override the toplevel setting in .bazelrc.
build:remote --remote_download_outputs=all
build --config=release --config=remote-intel --config=disable-mypy --config=local-gpu --//:kernel_e2e_gpu_profiling=true
run --config=release --config=disable-mypy
test --config=release --config=disable-mypy
"""
    run_ssh_command(
        ssh_client, f'echo "{local_bazlerc}" >> ~/work/modular/local.bazlrc'
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

    ssh_client.close()
    print("Installation and configuration completed.")

    os.system(f"ssh -i {key_path} {remote_username}@{vm_ip}")


if __name__ == "__main__":
    cli()
