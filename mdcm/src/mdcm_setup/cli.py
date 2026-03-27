"""Create and configure MDCM instance."""

import base64
import os
import sys
from pathlib import Path

import click
import paramiko
from paramiko.proxy import ProxyCommand


# --- Constants ---

REMOTE_USERNAME = "ubuntu"

# Timeouts (seconds).
DEFAULT_TIMEOUT = 120
LONG_TIMEOUT = 600

# Tool versions.
NVIM_VERSION = "v0.11.3"
DELTA_VERSION = "0.18.2"

# Architecture mappings for release downloads.
NVIM_ARCH = {"x86_64": "x86_64", "aarch64": "arm64"}
DELTA_ARCH = {"x86_64": "x86_64", "aarch64": "aarch64"}

# Sentinel comment for idempotent .zshrc epilogue.
ZSHRC_SENTINEL = "# MDCM_SETUP_EPILOGUE"

# Shell snippets for sourcing tools in non-login SSH sessions.
NVM_SOURCE = (
    'export NVM_DIR="$HOME/.nvm"'
    ' && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"'
)
CARGO_SOURCE = '[ -f "$HOME/.cargo/env" ] && . "$HOME/.cargo/env"'
PNPM_SOURCE = (
    'export PNPM_HOME="/home/ubuntu/.local/share/pnpm"'
    ' && export PATH="$PNPM_HOME:$PATH"'
)
PYENV_SOURCE = (
    'export PYENV_ROOT="$HOME/.pyenv"'
    ' && export PATH="$PYENV_ROOT/bin:$PATH"'
    ' && eval "$(pyenv init -)"'
)

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

# Load environment variables (including HF_TOKEN) from ~/.env.
[ -f ~/.env ] && source ~/.env
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
"""

GITCONFIG = """\
[blame]
  pager = delta

[core]
  editor = nvim -u ~/.config/nvim/init.lua
  pager = delta

[delta]
  features = calochortus-lyallii side-by-side
  line-numbers = false
  hyperlinks = true
  navigate = true
  light = false

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
  email = bduke@modular.com

[maintenance]
  repo = /home/ubuntu/work/modular
"""

BASE_APT_PACKAGES = (
    "expect xclip zsh protobuf-compiler fd-find pipx less libtbb-dev"
)

EXTRA_APT_PACKAGES = (
    "git-lfs make build-essential libssl-dev zlib1g-dev libbz2-dev"
    " libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev"
    " xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev"
)


# --- Core helpers ---


def run_ssh_command(ssh_client, command, timeout=DEFAULT_TIMEOUT, check=False):
    """Run a command over SSH, streaming output.

    Returns the exit status. If check=True, raises RuntimeError on non-zero
    exit.
    """
    chan = ssh_client.get_transport().open_session()
    chan.settimeout(timeout)
    chan.exec_command(command)

    stdout = chan.makefile("r")
    stderr = chan.makefile_stderr("r")

    for line in iter(stdout.readline, ""):
        print(line, end="")

    for line in iter(stderr.readline, ""):
        print(line, end="", file=sys.stderr)

    exit_status = chan.recv_exit_status()
    if exit_status != 0:
        msg = f"{command!r} failed with exit = {exit_status}"
        if check:
            raise RuntimeError(msg)
        print(msg)
    return exit_status


def run_ssh_command_capture(ssh_client, command, timeout=DEFAULT_TIMEOUT):
    """Run a command and return its stdout as a stripped string."""
    chan = ssh_client.get_transport().open_session()
    chan.settimeout(timeout)
    chan.exec_command(command)
    stdout = chan.makefile("r").read().strip()
    stderr = chan.makefile_stderr("r").read()
    exit_status = chan.recv_exit_status()
    if exit_status != 0:
        raise RuntimeError(
            f"{command!r} failed (exit {exit_status}): {stderr.strip()}"
        )
    return stdout


def find_coder_binary():
    """Find the coder binary on the local system."""
    candidates = [
        Path("~/.local/bin/coder").expanduser(),
        Path("/usr/local/bin/coder"),
        Path("/opt/homebrew/bin/coder"),
    ]
    for path in candidates:
        if path.exists():
            return str(path)
    raise FileNotFoundError(
        "coder binary not found. Searched: "
        + ", ".join(str(p) for p in candidates)
    )


def connect_ssh(vm_name):
    """Create SSH connection to a Coder VM via proxy.

    Returns (proxy, ssh_client). Caller must close both.
    """
    coder_bin = find_coder_binary()
    coder_config = Path("~/Library/Application Support/coderv2").expanduser()
    proxy_cmd = (
        f'{coder_bin} --global-config "{coder_config}"'
        f" ssh --stdio {vm_name}"
    )

    proxy = ProxyCommand(proxy_cmd)
    try:
        transport = paramiko.Transport(proxy)
        transport.start_client()
        # Coder proxy handles real authentication; paramiko just needs
        # auth_none.  SSHClient.connect() doesn't support auth_none
        # directly (even in paramiko 4.x), so we attach the transport
        # to the client manually.  _transport is a stable internal
        # attribute that has existed across all paramiko versions.
        transport.auth_none(REMOTE_USERNAME)

        ssh_client = paramiko.SSHClient()
        ssh_client._transport = transport

        # Verify connectivity.
        run_ssh_command(ssh_client, "echo 'Connection established'", check=True)
        return proxy, ssh_client
    except Exception:
        proxy.close()
        raise


def detect_arch(ssh_client):
    """Detect remote machine architecture (x86_64 or aarch64)."""
    return run_ssh_command_capture(ssh_client, "uname -m")


def clone_if_missing(ssh_client, gcl, url, dest, timeout=LONG_TIMEOUT):
    """Idempotent git clone.  Skips if dest already exists.

    dest may contain ~ or shell variable expansions.
    """
    run_ssh_command(
        ssh_client,
        f"[ -d {dest} ] && echo 'Skipping clone, {dest} exists'"
        f" || ({gcl} {url} {dest})",
        timeout=timeout,
        check=True,
    )


# --- Setup phase functions ---


def upload_local_files(ssh_client, *, upload_ssh_key=False):
    """Upload .env file and optionally SSH key to the remote host."""
    run_ssh_command(
        ssh_client, "mkdir -p ~/.ssh && chmod 700 ~/.ssh", check=True
    )

    with ssh_client.open_sftp() as sftp:
        if upload_ssh_key:
            local_key = Path("~/.ssh/id_ed25519").expanduser()
            if local_key.exists():
                sftp.put(str(local_key), ".ssh/id_ed25519")
                sftp.chmod(".ssh/id_ed25519", 0o600)

        local_env = Path.home() / ".env"
        if local_env.exists():
            sftp.put(str(local_env), ".env")
            sftp.chmod(".env", 0o600)


def setup_locale(ssh_client):
    """Configure en_CA.UTF-8 locale."""
    run_ssh_command(
        ssh_client,
        "sudo sed -i 's/# en_CA.UTF-8 UTF-8/en_CA.UTF-8 UTF-8/'"
        " /etc/locale.gen",
    )
    run_ssh_command(ssh_client, "sudo locale-gen")
    run_ssh_command(ssh_client, "sudo update-locale LANG=en_CA.UTF-8")


def install_apt_packages(ssh_client, *, extra_packages=""):
    """Update apt and install base packages, plus any extras."""
    apt = "DEBIAN_FRONTEND=noninteractive apt-get"
    packages = BASE_APT_PACKAGES
    if extra_packages:
        packages += " " + extra_packages

    run_ssh_command(
        ssh_client,
        f"sudo {apt} update && sudo {apt} -y upgrade",
        timeout=LONG_TIMEOUT,
    )
    run_ssh_command(
        ssh_client,
        f"sudo {apt} install -y {packages}",
        timeout=LONG_TIMEOUT,
    )
    run_ssh_command(ssh_client, "pipx install stack-pr")


def install_oh_my_zsh(ssh_client):
    """Install and configure oh-my-zsh."""
    run_ssh_command(ssh_client, "sudo passwd -d $(whoami)")
    run_ssh_command(ssh_client, "sudo chsh -s $(which zsh)")
    run_ssh_command(
        ssh_client,
        "curl -fsSL"
        " https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
        " -o install_oh_my_zsh.sh",
    )
    run_ssh_command(ssh_client, "chmod +x install_oh_my_zsh.sh")

    # Write expect script via SFTP to avoid shell escaping issues.
    expect_script = (
        "#!/usr/bin/expect\n"
        "set timeout 30\n"
        'spawn sh -c "./install_oh_my_zsh.sh"\n'
        'expect "Do you want to change your default shell to zsh?"\n'
        'send "y\\r"\n'
        "expect eof\n"
    )
    with ssh_client.open_sftp() as sftp:
        with sftp.open("install_oh_my_zsh.expect", "w") as f:
            f.write(expect_script)

    run_ssh_command(ssh_client, "chmod +x install_oh_my_zsh.expect")
    run_ssh_command(
        ssh_client, "rm -rf ~/.oh-my-zsh && ./install_oh_my_zsh.expect"
    )


def install_neovim(ssh_client, arch):
    """Install neovim for the detected architecture."""
    nvim_arch = NVIM_ARCH.get(arch, "x86_64")
    tarball = f"nvim-linux-{nvim_arch}.tar.gz"
    url = (
        "https://github.com/neovim/neovim/releases/download/"
        f"{NVIM_VERSION}/{tarball}"
    )

    run_ssh_command(ssh_client, f"curl -fsSL {url} -o {tarball}")
    run_ssh_command(ssh_client, f"tar zxf {tarball}")
    run_ssh_command(
        ssh_client,
        f"sudo ln -sf $(pwd)/nvim-linux-{nvim_arch}/bin/nvim"
        " /usr/local/bin/nvim",
    )


def install_llvm_toolchain(ssh_client, vm_name, *, install_from_apt=True):
    """Install LLVM toolchain and set up compiler alternatives."""
    if install_from_apt and "c7g" not in vm_name:
        run_ssh_command(
            ssh_client,
            'sudo bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"',
            timeout=LONG_TIMEOUT,
        )
    run_ssh_command(
        ssh_client,
        "sudo update-alternatives --install /usr/bin/cc cc"
        " /usr/bin/clang 100 && "
        "sudo update-alternatives --install /usr/bin/c++ c++"
        " /usr/bin/clang++ 100",
    )


def configure_shell_and_git(ssh_client):
    """Configure zsh plugins, .zshrc epilogue, and .gitconfig."""
    # Add vi-mode plugin to oh-my-zsh.
    run_ssh_command(
        ssh_client,
        "sed -i 's/plugins=(git)/plugins=(git vi-mode)/' ~/.zshrc",
    )

    # Append sentinel-guarded epilogue (idempotent: skips if already present).
    epilogue_with_sentinel = f"{ZSHRC_SENTINEL}\n{ZSHRC_EPILOGUE}"
    epilogue_b64 = base64.b64encode(
        epilogue_with_sentinel.encode()
    ).decode()
    run_ssh_command(
        ssh_client,
        f"grep -q '{ZSHRC_SENTINEL}' ~/.zshrc 2>/dev/null"
        f' || echo "{epilogue_b64}" | base64 --decode >> ~/.zshrc',
    )

    # Write .gitconfig.
    gitconfig_b64 = base64.b64encode(GITCONFIG.encode()).decode()
    run_ssh_command(
        ssh_client,
        f'echo "{gitconfig_b64}" | base64 --decode > ~/.gitconfig',
    )


def install_dev_tools(ssh_client, *, gcl, arch):
    """Install dev tools: pyenv, pnpm, nvm, node, cargo, LSPs, delta, fzf."""
    # --- pyenv (skip clone if already installed) ---
    run_ssh_command(
        ssh_client,
        '[ -d "$HOME/.pyenv" ] || (curl https://pyenv.run | bash)',
        timeout=LONG_TIMEOUT,
    )
    # -s flag skips if version already installed.
    run_ssh_command(
        ssh_client,
        f"{PYENV_SOURCE} && pyenv install -s 3.12",
        timeout=LONG_TIMEOUT,
    )

    # --- install-llvm.sh from the modular repo ---
    run_ssh_command(
        ssh_client,
        "cd ~/work/modular && ./utils/install-llvm.sh",
        timeout=LONG_TIMEOUT,
    )

    # --- pnpm ---
    run_ssh_command(
        ssh_client,
        "curl -fsSL https://get.pnpm.io/install.sh | sh -",
        timeout=LONG_TIMEOUT,
    )

    # --- nvm + node (source nvm before using it) ---
    run_ssh_command(
        ssh_client,
        "curl -o-"
        " https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh"
        " | bash",
        timeout=LONG_TIMEOUT,
    )
    run_ssh_command(
        ssh_client,
        f"{NVM_SOURCE} && nvm install node",
        timeout=LONG_TIMEOUT,
    )

    # --- bazelrc-lsp (source pnpm before using it) ---
    clone_if_missing(
        ssh_client,
        gcl,
        "git@github.com:salesforce-misc/bazelrc-lsp",
        "~/work/bazelrc-lsp",
    )
    run_ssh_command(
        ssh_client,
        f"{PNPM_SOURCE} && cd ~/work/bazelrc-lsp/vscode-extension"
        " && pnpm i && pnpm package",
        timeout=LONG_TIMEOUT,
    )

    # --- bazel-lsp ---
    clone_if_missing(
        ssh_client,
        gcl,
        "git@github.com:cameron-martin/bazel-lsp",
        "~/work/bazel-lsp",
    )
    run_ssh_command(
        ssh_client,
        "cd ~/work/bazel-lsp && bazel build //:bazel-lsp -c opt",
        timeout=LONG_TIMEOUT,
    )

    # --- ibazel ---
    clone_if_missing(
        ssh_client,
        gcl,
        "git@github.com:bazelbuild/bazel-watcher",
        "~/work/bazel-watcher",
    )
    run_ssh_command(
        ssh_client,
        "cd ~/work/bazel-watcher && bazel build //cmd/ibazel",
        timeout=LONG_TIMEOUT,
    )

    # --- delta (arch-aware) ---
    run_ssh_command(ssh_client, "mkdir -p ~/.local/bin")
    delta_arch = DELTA_ARCH.get(arch, "x86_64")
    delta_dir = f"delta-{DELTA_VERSION}-{delta_arch}-unknown-linux-gnu"
    delta_tarball = f"{delta_dir}.tar.gz"
    delta_url = (
        "https://github.com/dandavison/delta/releases/download/"
        f"{DELTA_VERSION}/{delta_tarball}"
    )
    run_ssh_command(
        ssh_client,
        f"cd ~/work && curl -fSsL {delta_url} -o {delta_tarball}"
        f" && tar zxvf {delta_tarball}"
        f" && ln -sf $(pwd)/{delta_dir}/delta ~/.local/bin/delta",
    )

    # --- cargo + tools (source cargo env before using) ---
    run_ssh_command(
        ssh_client,
        "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs"
        " | sh -s -- -y",
        timeout=LONG_TIMEOUT,
    )
    run_ssh_command(
        ssh_client,
        f"{CARGO_SOURCE} && cargo install tokei",
        timeout=LONG_TIMEOUT,
    )
    run_ssh_command(
        ssh_client,
        f"{CARGO_SOURCE} && cargo install --locked tree-sitter-cli",
        timeout=LONG_TIMEOUT,
    )

    # --- pip tools ---
    run_ssh_command(
        ssh_client,
        "pip install --upgrade pip debugpy pynvim nvitop",
    )

    # --- fzf (skip if already cloned) ---
    run_ssh_command(
        ssh_client,
        "[ -d ~/.fzf ] || (git clone --depth 1"
        " https://github.com/junegunn/fzf.git ~/.fzf"
        " && ~/.fzf/install --all --no-bash --no-fish --no-update-rc)",
    )


def upload_config_scripts(ssh_client, *, include_claude_tmux=False):
    """Upload codex/claude config scripts to the remote host."""
    run_ssh_command(
        ssh_client, "mkdir -p ~/.local/bin ~/.codex", check=True
    )

    files_dir = Path(__file__).parent / "files"

    uploads = [
        ("codex-tmux", ".local/bin/codex-tmux", 0o755),
        ("tmux-codex.conf", ".local/bin/tmux-codex.conf", 0o644),
        ("codex-init-session", ".local/bin/codex-init-session", 0o755),
        ("AGENTS.md", ".codex/AGENTS.md", 0o644),
        ("config.toml", ".codex/config.toml", 0o644),
    ]
    if include_claude_tmux:
        uploads.append(("claude-tmux", ".local/bin/claude-tmux", 0o755))

    with ssh_client.open_sftp() as sftp:
        for filename, remote_path, mode in uploads:
            local_path = files_dir / filename
            if local_path.exists():
                sftp.put(str(local_path), remote_path)
                sftp.chmod(remote_path, mode)


def setup_vim_syntax(ssh_client, remote_work_dir="~/work"):
    """Set up MLIR/LLVM/Mojo vim syntax highlighting (requires modular)."""
    # Trigger LLVM download via bazel.
    run_ssh_command(
        ssh_client,
        f"cd {remote_work_dir}/modular && ./bazelw query"
        " @llvm-project//... --keep_going --noshow_progress"
        " 2>/dev/null || true",
        timeout=LONG_TIMEOUT,
    )

    # MLIR syntax.
    run_ssh_command(
        ssh_client,
        (
            f"cd {remote_work_dir}/modular && "
            "LLVM_PATH=bazel-modular/external/+http_archive+llvm-raw && "
            "if [ -d $LLVM_PATH/mlir/utils/vim ]; then "
            "  for FOLDER in ftdetect ftplugin indent syntax; do "
            "    mkdir -p ~/.config/nvim/$FOLDER && "
            "    [ -f $LLVM_PATH/mlir/utils/vim/$FOLDER/mlir.vim ] && "
            "    ln -sf $(pwd)/$LLVM_PATH/mlir/utils/vim/$FOLDER/mlir.vim"
            " ~/.config/nvim/$FOLDER/mlir.vim; "
            "  done; "
            "fi"
        ),
    )

    # LLVM syntax (tablegen, llvm, llvm-lit, mir).
    for filetype in ["tablegen", "llvm", "llvm-lit", "mir"]:
        run_ssh_command(
            ssh_client,
            (
                f"cd {remote_work_dir}/modular && "
                "LLVM_PATH=bazel-modular/external/+http_archive+llvm-raw && "
                "if [ -d $LLVM_PATH/llvm/utils/vim ]; then "
                "  for FOLDER in ftdetect ftplugin indent syntax; do "
                "    mkdir -p ~/.config/nvim/$FOLDER && "
                f"    [ -f $LLVM_PATH/llvm/utils/vim/$FOLDER/{filetype}.vim ]"
                f" && ln -sf $(pwd)/$LLVM_PATH/llvm/utils/vim/$FOLDER/"
                f"{filetype}.vim ~/.config/nvim/$FOLDER/{filetype}.vim; "
                "  done; "
                "fi"
            ),
        )

    # Mojo syntax.
    run_ssh_command(
        ssh_client,
        (
            f"cd {remote_work_dir}/modular && "
            "for FOLDER in autoload ftdetect ftplugin indent syntax; do "
            "  mkdir -p ~/.config/nvim/$FOLDER && "
            "  [ -f utils/mojo/vim/$FOLDER/mojo.vim ] && "
            "  ln -sf $(pwd)/utils/mojo/vim/$FOLDER/mojo.vim"
            " ~/.config/nvim/$FOLDER/mojo.vim; "
            "done"
        ),
    )


def setup_cuda_symlink(ssh_client):
    """Create CUDA library symlink."""
    run_ssh_command(
        ssh_client,
        "sudo mkdir -p /usr/local/cuda/lib64 && "
        "sudo ln -sf"
        " /usr/local/cuda-12.6/targets/x86_64-linux/lib/libnvToolsExt.so"
        " /usr/local/cuda/lib64/libnvToolsExt.so",
    )


# --- CLI commands ---


@click.group()
def cli():
    """CLI commands."""


@cli.command()
@click.option("--vm-name", type=str, required=True, help="Name of the VM")
def install_configure(vm_name):
    """SSH into the VM and run full install and configuration."""
    gcl = (
        "GIT_SSH_COMMAND='ssh -o StrictHostKeyChecking=no'"
        " git clone --recurse-submodules"
    )
    remote_work_dir = "~/work"

    proxy, ssh_client = connect_ssh(vm_name)
    try:
        arch = detect_arch(ssh_client)

        upload_local_files(ssh_client, upload_ssh_key=True)
        setup_locale(ssh_client)
        install_apt_packages(ssh_client, extra_packages=EXTRA_APT_PACKAGES)
        install_oh_my_zsh(ssh_client)
        install_neovim(ssh_client, arch)

        # Clone repositories.
        run_ssh_command(
            ssh_client, f"mkdir -p {remote_work_dir}", check=True
        )
        clone_if_missing(
            ssh_client,
            gcl,
            "git@github.com:dukebw/random-vimrc-etc",
            f"{remote_work_dir}/random-vimrc-etc",
        )
        clone_if_missing(
            ssh_client,
            gcl,
            "git@github.com:dukebw/kickstart.nvim.git",
            '"${XDG_CONFIG_HOME:-$HOME/.config}"/nvim',
        )
        clone_if_missing(
            ssh_client,
            gcl,
            "git@github.com:modularml/modular",
            f"{remote_work_dir}/modular",
        )

        # Bootstrap modular development environment.
        run_ssh_command(
            ssh_client,
            f"cd {remote_work_dir}/modular"
            " && source utils/start-modular.sh && install_dev_deps",
            timeout=LONG_TIMEOUT,
        )

        # Vim syntax highlighting (requires modular repo + bazel).
        setup_vim_syntax(ssh_client, remote_work_dir)

        # Copy personal config files.
        run_ssh_command(
            ssh_client,
            f"cp {remote_work_dir}/random-vimrc-etc/local.bazelrc"
            f" {remote_work_dir}/modular",
        )
        run_ssh_command(
            ssh_client,
            f"cp {remote_work_dir}/random-vimrc-etc/.nvim-dap.json"
            f" {remote_work_dir}/modular",
        )

        install_llvm_toolchain(
            ssh_client, vm_name, install_from_apt=True
        )
        configure_shell_and_git(ssh_client)
        install_dev_tools(ssh_client, gcl=gcl, arch=arch)
        upload_config_scripts(ssh_client)
        setup_cuda_symlink(ssh_client)

        print("Installation and configuration completed.")
    finally:
        ssh_client.close()
        proxy.close()

    # Open interactive SSH after closing paramiko to avoid dangling
    # connection.
    os.system(f"ssh -Y coder.{vm_name}")


@cli.command()
@click.option(
    "--vm-name", type=str, default="bduke-a100", help="Name of the VM"
)
def coder(vm_name):
    """SSH into the VM and run install and configuration commands."""
    gcl = "git clone --recurse-submodules"
    remote_work_dir = "~/work"

    proxy, ssh_client = connect_ssh(vm_name)
    try:
        arch = detect_arch(ssh_client)

        upload_local_files(ssh_client)
        setup_locale(ssh_client)
        install_apt_packages(ssh_client)
        install_oh_my_zsh(ssh_client)
        install_neovim(ssh_client, arch)

        # Clone repositories (fixed: modular must be cloned before
        # install-llvm.sh runs in install_dev_tools).
        run_ssh_command(
            ssh_client, f"mkdir -p {remote_work_dir}", check=True
        )
        clone_if_missing(
            ssh_client,
            gcl,
            "git@github.com:dukebw/random-vimrc-etc",
            f"{remote_work_dir}/random-vimrc-etc",
        )
        clone_if_missing(
            ssh_client,
            gcl,
            "git@github.com:dukebw/kickstart.nvim.git",
            '"${XDG_CONFIG_HOME:-$HOME/.config}"/nvim',
        )
        clone_if_missing(
            ssh_client,
            gcl,
            "git@github.com:modularml/modular",
            f"{remote_work_dir}/modular",
        )

        # Bootstrap modular development environment.
        run_ssh_command(
            ssh_client,
            f"cd {remote_work_dir}/modular"
            " && source utils/start-modular.sh && install_dev_deps",
            timeout=LONG_TIMEOUT,
        )

        install_llvm_toolchain(
            ssh_client, vm_name, install_from_apt=False
        )
        configure_shell_and_git(ssh_client)
        install_dev_tools(ssh_client, gcl=gcl, arch=arch)
        upload_config_scripts(ssh_client, include_claude_tmux=True)
        setup_cuda_symlink(ssh_client)

        print("Installation and configuration completed.")
    finally:
        ssh_client.close()
        proxy.close()

    os.system(f"ssh -Y coder.{vm_name}")


if __name__ == "__main__":
    cli()
