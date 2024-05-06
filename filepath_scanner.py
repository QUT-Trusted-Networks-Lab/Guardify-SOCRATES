import subprocess
import re
import select
import os
import json
from datetime import datetime
from config_loader import ConfigLoader, ConfigLoaderError

def load_filters(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def check_path_against_filters(path, filters):
    for filter_type in ['greylist', 'blacklist']:
        for filter_path in filters[filter_type]:
            if path.startswith(filter_path):
                return filter_type
    return None

def monitor(config):
    filters_file_path = config['plugins']['file_path_checks']['paths_config_file']
    filters = load_filters(filters_file_path)

    print("[INFO] Monitoring system calls...")

    cmd = ["sudo", "sh", "-c", "BPFTRACE_STRLEN=150 bpftrace -v filepath_trace_engine.bt"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

    log_directory = config['plugins']['file_path_checks']['log_directory']
    full_log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_directory)

    if not os.path.exists(full_log_directory):
        os.makedirs(full_log_directory)

    current_time = datetime.now().strftime('%d%b%Y_%I:%M:%S%p')
    filename = f'{full_log_directory}/file_filepath{current_time}.log'
    warning_filename = f'{full_log_directory}/file_filepath{current_time}_warning.log'

    with open(filename, 'w') as log_file:
        log_buffer = []
        while True:
            readable, _, _ = select.select([process.stdout, process.stderr], [], [])
            for pipe in readable:
                line = pipe.readline()
                if not line:
                    continue

                if pipe is process.stdout:
                    log_buffer.append(line)

                    matches = re.findall(r'(\d{2}:\d{2}:\d{2})\s+([\w\d]+)\s+(\d+)\s+([\w\d_]+)\s+->\s*([^,\n]+)', line)
                    for match in matches:
                        time, comm, pid, tracepoint, path = match
                        path = path.strip()

                        result = check_path_against_filters(path, filters)
                        if result:
                            warning_msg = f"WARNING: {time} {comm} {pid} {tracepoint} -> {path} matches the {result}!"
                            print(warning_msg)
                            with open(warning_filename, 'a') as warning_file:
                                warning_file.write(warning_msg + '\n')

                elif pipe is process.stderr:
                    print(f"[NOTE] {line}", end='')

                if len(log_buffer) > 100:
                    log_file.writelines(log_buffer)
                    log_buffer.clear()
                    log_file.flush()

    if log_buffer:
        log_file.writelines(log_buffer)
        log_file.flush()

if __name__ == "__main__":
    try:
        loader = ConfigLoader()
        config = loader.load_config()
        monitor(config)
    except ConfigLoaderError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[INFO] Script interrupted. Exiting...")
    finally:
        if 'process' in locals() and process.poll() is None:
            process.terminate()
            process.wait()
        os.system('reset')
