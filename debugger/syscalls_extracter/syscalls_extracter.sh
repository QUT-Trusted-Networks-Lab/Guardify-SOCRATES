#!/bin/bash

# File to store the list of syscalls
AVAILABLE_SYSCALLS="available_syscalls.txt"
# File to store syscall arguments
SYSCALLS_ARGS="syscalls_args.txt"

# Clear or create the files
> $AVAILABLE_SYSCALLS
> $SYSCALLS_ARGS

# Extract syscalls
syscalls=$(sudo bpftrace -l 'tracepoint:syscalls:sys_enter_*' | sort)

# Save syscalls
echo "$syscalls" > $AVAILABLE_SYSCALLS

# Loop through syscalls and extract arguments
for syscall in $syscalls; do
    echo "Arguments for $syscall:" >> $SYSCALLS_ARGS
    sudo bpftrace -lv $syscall >> $SYSCALLS_ARGS
    echo "" >> $SYSCALLS_ARGS
done

echo "Syscall extraction complete."
