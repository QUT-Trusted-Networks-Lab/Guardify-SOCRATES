import sys
import re
import tarfile
import subprocess
import json
import logging
import datetime
import os
from config_loader import ConfigLoader, ConfigLoaderError

def setup_logging(log_directory):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    logging.basicConfig(filename=os.path.join(log_directory, 'guardify.log'),
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def load_suspect_keywords(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        error_message = f"Error: Keyword file {file_path} not found."
        logging.error(error_message)
        sys.stderr.write(error_message + "\n")
        sys.exit(1)

def check_typo_squatting(package_name, suspect_keywords):
    return any(keyword in package_name for keyword in suspect_keywords)

def load_obfuscation_patterns(patterns_file):
    try:
        with open(patterns_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        error_message = f"Error loading obfuscation patterns: {e}"
        logging.error(error_message)
        sys.stderr.write(error_message + "\n")
        sys.exit(1)

def scan_tarball_for_obfuscation(tar_path, patterns):
    with tarfile.open(tar_path, 'r:gz') as tar:
        print(f"Scanning tarball: {tar_path}")  # Debugging line
        for member in tar.getmembers():
            if member.isfile() and member.name.endswith('.py'):
                print(f"Checking file: {member.name}")  # Debugging line
                with tar.extractfile(member) as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    for pattern_name, pattern in patterns.items():
                        if re.search(pattern, content):
                            print(f"Pattern '{pattern_name}' found in file: {member.name}")  # Debugging line
                            return True, pattern_name, member.name
    return False, None, None

def setup_specific_logger(log_directory, log_type, package_manager, package_name, log_level):
    # Create directory if it does not exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Format the filename: e.g., pip_packagename_8_April_2024_11:54:53AM.log
    timestamp = datetime.datetime.now().strftime("%d_%B_%Y_%H:%M:%S:%p")
    filename = f"{package_manager}_{package_name}_{timestamp}.log".replace('.tar.gz', '')

    # Setup logging
    specific_logger = logging.getLogger(log_type + filename)  # Unique logger per file
    handler = logging.FileHandler(os.path.join(log_directory, filename))
    handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    specific_logger.addHandler(handler)
    specific_logger.propagate = False

    return specific_logger

def guardify_install(command, config):
    logging.info("Guardify Install command started.")

    if len(command) >= 3 and command[1] == 'pip' and command[2] == 'install':
        package_path = command[3]
        package_name = package_path.split('/')[-1]

        # Typo Squatting Check
        if config['typo_squatting']['enabled']:
            pip_config = config['typo_squatting']['package_managers']['pip']
            if pip_config['enabled']:
                keywords = load_suspect_keywords(pip_config['suspect_keywords_file'])
                if check_typo_squatting(package_name, keywords):
                    warning_message = f"Potential typo squatting detected for package {package_name}."

                    # Fetch log directory from config
                    log_directory = config['typo_squatting']['log_directory']

                    typo_squatting_logger = setup_specific_logger(
                        log_directory, 'typo_squatting', 'pip', package_name, logging.WARNING
                    )
                    typo_squatting_logger.warning(warning_message)
                    print(f"Warning: {warning_message}")

        # Obfuscation Check
        if config['code_obfuscation']['enabled'] and package_path.endswith('.tar.gz'):
            patterns_file = config['code_obfuscation']['obfuscation_patterns_file']
            patterns = load_obfuscation_patterns(patterns_file)
            detected, pattern_name, obfuscated_file = scan_tarball_for_obfuscation(package_path, patterns)
            if detected:
                alert_message = f"Obfuscation pattern '{pattern_name}' detected in file {obfuscated_file} of {package_name}."
                print(alert_message)

                # Fetch log directory from config
                obfuscation_log_directory = config['code_obfuscation']['log_directory']

                obfuscation_logger = setup_specific_logger(
                    obfuscation_log_directory, 'obfuscation', 'pip', package_name, logging.WARNING
                )
                obfuscation_logger.warning(alert_message)
                logging.warning(alert_message)  # Additional logging for better visibility

                response = input("Proceed with installation? [y/N]: ")
                if response.lower() != 'y':
                    print("Installation aborted.")
                    obfuscation_logger.info("Installation aborted by user.")
                    return
                else:
                    obfuscation_logger.info("User opted to proceed with installation despite warnings.")

        # Proceed with pip installation
        try:
            subprocess.run(["pip", "install", package_path], check=True)
            logging.info(f"Package {package_name} installed successfully.")
        except subprocess.CalledProcessError as e:
            error_message = f"Error during installation of {package_name}: {e}"
            sys.stderr.write(error_message + "\n")
            logging.error(error_message)
            sys.exit(1)

if __name__ == "__main__":
    try:
        loader = ConfigLoader()
        config = loader.load_config()
        setup_logging(config['global']['log_directory'])
        guardify_install(sys.argv, config)
    except ConfigLoaderError as e:
        error_message = f"Configuration error: {e}"
        sys.stderr.write(error_message + "\n")
        logging.error(error_message)
        sys.exit(1)