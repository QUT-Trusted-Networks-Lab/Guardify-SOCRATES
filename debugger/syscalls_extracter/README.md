Syscall Extractor Script
Introduction
This script is designed to extract and list all available system calls and their arguments on a Linux system using bpftrace. It generates two output files: one with a list of syscalls and another with their arguments.

Prerequisites
A Linux system
bpftrace installed
Installation
Install bpftrace:
For Ubuntu/Debian:
sudo apt-get update
sudo apt-get install bpftrace

For other distributions, refer to your package manager or compile from source.

Clone the repository or download the script extract_syscalls.sh.

Make the script executable:
chmod +x extract_syscalls.sh

Usage
Run the script with:
./extract_syscalls.sh

This will create two files in the current directory:

available_syscalls.txt: Contains a list of all available syscalls.
syscalls_args.txt: Lists the arguments for each syscall.
Output Files
available_syscalls.txt: A simple list of all syscalls available on the system.
syscalls_args.txt: Detailed information about each syscall, including the arguments it takes.
Note
The script requires sudo privileges to access bpftrace functionality.
