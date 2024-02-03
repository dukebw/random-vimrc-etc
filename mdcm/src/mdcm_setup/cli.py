"""Create and configure MDCM instance."""
import os
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
@click.option("--vm-name", type=str, default="c6i.16xlarge", help="Name of the VM")
def create_vm(vm_name: str):
    """Create and start the VM."""
    run_local_command(f"mdcm volume create --name {volume_name} --size {volume_size}")
    run_local_command(
        f"mdcm vm create -n {vm_name} -t {instance_type} -osver {os_version} -v"
        f" {volume_name}"
    )
    run_local_command(f"mdcm vm start --name {vm_name}")
    print(f"VM {vm_name} created and started.")


@cli.command()
@click.option("--vm-ip", type=str, required=True, help="IP address of the VM")
@click.option("--vm-name", type=str, default="c6i.16xlarge", help="Name of the VM")
def install_configure(vm_ip: str, vm_name: str):
    """SSH into the VM and run install and configuration commands."""
    local_home_dir = Path(os.getenv("HOME"))
    key_path = local_home_dir / ".ssh" / "mdcm.pem"
    remote_work_dir = "~/work"

    # SSH into the VM
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(vm_ip, username=remote_username, key_filename=str(key_path))

    # Update and install oh-my-zsh
    run_ssh_command(ssh_client, "sudo apt update && sudo apt upgrade -y")
    run_ssh_command(ssh_client, "sudo apt install -y expect zsh")
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
    run_ssh_command(ssh_client, f"echo -e '{expect_script}' > install_oh_my_zsh.expect")
    run_ssh_command(ssh_client, "chmod +x install_oh_my_zsh.expect")
    run_ssh_command(ssh_client, "./install_oh_my_zsh.expect")

    # Copy SSH keys to VM
    run_local_command(
        f"scp -o 'StrictHostKeyChecking=no' -i {str(key_path)} ~/.ssh/id_ed25519*"
        f" {remote_username}@{vm_ip}:.ssh"
    )

    # Install neovim
    if "c6g" in vm_name:
        # Install neovim from source.
        run_ssh_command(
            ssh_client, "sudo apt install -y ninja-build gettext cmake unzip curl"
        )
        run_ssh_command(
            ssh_client,
            (
                "curl -fsSL"
                " https://github.com/neovim/neovim/archive/refs/tags/v0.9.4.tar.gz -o"
                " nvim-v0.9.4.tar.gz && tar zxf nvim-v0.9.4.tar.gz && cd neovim-0.9.4"
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
                " https://github.com/neovim/neovim/releases/download/nightly/nvim-linux64.tar.gz"
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
        ssh_client, "nvim -c 'PlugUpgrade | PlugInstall | PlugUpdate | qa!'", timeout=30
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
    run_ssh_command(
        ssh_client,
        (
            f"cd {remote_work_dir}/modular && for FOLDER in autoload ftdetect"
            " ftplugin indent syntax; do mkdir -p ~/.config/nvim/$FOLDER && ln -s"
            " $(pwd)/utils/mojo/vim/$FOLDER/mojo.vim ~/.config/nvim/$FOLDER/mojo.vim;"
            " done"
        ),
    )

    run_ssh_command(
        ssh_client,
        (
            'sudo bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)" && '
            "sudo update-alternatives --install /usr/bin/cc cc /usr/bin/clang 100 && "
            "sudo update-alternatives --install /usr/bin/c++ c++ /usr/bin/clang++ 100"
        ),
    )

    ssh_client.close()
    print("Installation and configuration completed.")

    os.system(f"ssh -i {key_path} {remote_username}@{vm_ip}")


if __name__ == "__main__":
    cli()
