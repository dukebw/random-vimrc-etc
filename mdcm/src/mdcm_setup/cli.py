"""Create and configure MDCM instance."""
import os
import subprocess
from pathlib import Path

import click
import paramiko

# Define constants
vm_name = "c6g.16xlarge"
vm_ip = "18.118.164.188"  # Replace with the dynamic IP if needed
key_path = Path(os.getenv("HOME")) / f"mdcm_keys/bduke-dev-it-{vm_name}-key.pem"
remote_username = "ubuntu"
volume_name = "bduke-intel-500"
volume_size = 500
instance_type = "c5.12xlarge"
os_version = "22.04"

# Function to run local commands


def run_local_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error: {stderr}")
        exit(1)
    return stdout

# Function to execute remote commands via SSH


def run_ssh_command(ssh_client, command):
    print(command)
    _, stdout, stderr = ssh_client.exec_command(command)

    # Continuously read and print stdout
    for line in iter(stdout.readline, ""):
        print(line, end="")

    # Check for any errors
    error_output = stderr.read().decode()
    if error_output:
        print(f"Error: {error_output}")

    return stdout.channel.recv_exit_status()


@ click.group()
def cli():
    pass


@ cli.command()
def create_vm():
    """Create and start the VM."""
    run_local_command(f"mdcm volume create --name {volume_name} --size {volume_size}")
    run_local_command(f"mdcm vm create -n {vm_name} -t {instance_type} -osver {os_version} -v {volume_name}")
    run_local_command(f"mdcm vm start --name {vm_name}")
    print(f"VM {vm_name} created and started.")


@ cli.command()
@ click.option("--vm-ip", type=str, required=True, help="IP address of the VM")
def install_configure(vm_ip: str):
    """SSH into the VM and run install and configuration commands."""
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
        ssh_client, "curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -o install_oh_my_zsh.sh")
    run_ssh_command(ssh_client, "chmod +x install_oh_my_zsh.sh")

    expect_script = (
        "#!/usr/bin/expect\n"
        "set timeout 5\n"
        "spawn sh -c \"./install_oh_my_zsh.sh\"\n"
        "expect \"Do you want to change your default shell to zsh?\"\n"
        "send \"y\\r\"\n"
        "expect eof\n"
    )
    # Creating the Expect script on the remote machine
    run_ssh_command(ssh_client, f"echo -e '{expect_script}' > install_oh_my_zsh.expect")
    run_ssh_command(ssh_client, "chmod +x install_oh_my_zsh.expect")
    run_ssh_command(ssh_client, "./install_oh_my_zsh.expect")

    # Install neovim
    run_ssh_command(
        ssh_client, "curl -fsSL https://github.com/neovim/neovim/releases/download/nightly/nvim-linux64.tar.gz -o nvim-linux64.tar.gz")
    run_ssh_command(ssh_client, "tar zxf nvim-linux64.tar.gz")
    run_ssh_command(ssh_client, "sudo cp nvim-linux64/bin/nvim /usr/local/bin")

    # Configure neovim
    run_ssh_command(ssh_client, "mkdir -p ~/work && git clone git@github.com:dukebw/random-vimrc-etc ~/work/random-vimrc-etc")
    run_ssh_command(ssh_client, "mkdir -p ~/.config/nvim && cp ~/work/random-vimrc-etc/init.vim ~/.config/nvim")

    # Copy SSH keys to VM
    run_local_command(
        f"scp -o 'StrictHostKeyChecking=no' -i {str(key_path)} ~/.ssh/id_ed25519* {remote_username}@{vm_ip}:.ssh")

    # Perform final setup
    run_ssh_command(
        ssh_client, f"cd /mnt/{vm_name}-volume && git clone git@github.com:modularml/modular && cd modular && source utils/start-modular.sh && install_python_deps && install_dev_deps")

    ssh_client.close()
    print("Installation and configuration completed.")


if __name__ == '__main__':
    cli()
