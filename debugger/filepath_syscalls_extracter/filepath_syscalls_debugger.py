import subprocess

# List of specific tracepoints to check
specific_tracepoints = [
    "sys_enter_open", "sys_enter_openat", "sys_enter_creat", "sys_enter_access", "sys_enter_execv",
    "sys_enter_stat", "sys_enter_newstat", "sys_enter_lstat", "sys_enter_newlstat",
    "sys_enter_newfstatat", "sys_enter_readlink", "sys_enter_readlinkat",
    "sys_enter_rename", "sys_enter_renameat", "sys_enter_link", "sys_enter_linkat",
    "sys_enter_unlink", "sys_enter_unlinkat", "sys_enter_symlink", "sys_enter_symlinkat",
    "sys_enter_mknod", "sys_enter_mknodat", "sys_enter_chmod", "sys_enter_fchmodat",
    "sys_enter_chown", "sys_enter_lchown", "sys_enter_fchownat"
]

def check_tracepoints_and_arguments():
    available_tracepoints = []
    tracepoint_arguments = {}
    
    for tracepoint in specific_tracepoints:
        try:
            # Use bpftrace -lv for each specific tracepoint
            output = subprocess.check_output(["bpftrace", "-lv", f"tracepoint:syscalls:{tracepoint}"], text=True)
            if output.strip():  # Check if there's any output (tracepoint exists)
                available_tracepoints.append(tracepoint)
                tracepoint_arguments[tracepoint] = output
        except subprocess.CalledProcessError:
            pass  # Tracepoint doesn't exist, so no output
    
    return available_tracepoints, tracepoint_arguments

if __name__ == "__main__":
    tracepoints, arguments = check_tracepoints_and_arguments()
    
    if tracepoints:
        with open("tracepoints_debug.log", "w") as log_file:
            log_file.write("Available Tracepoints:\n")
            for tracepoint in tracepoints:
                log_file.write(tracepoint + "\n")
            log_file.write("\nArguments for Available Tracepoints:\n")
            for tracepoint, arg_info in arguments.items():
                log_file.write(f"{arg_info}\n")
        print("Available Tracepoints and their arguments have been saved to tracepoints_debug.log")
    else:
        print("No tracepoints found.")


