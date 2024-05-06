Guardify: A Comprehensive Python Package Security Tool
Guardify is a robust Python package security tool designed to protect your Python projects from various security threats. It provides a set of features to detect and prevent issues like obfuscation, typosquatting, suspicious file path access, and malicious network activity.
Table of Contents

Installation
Usage

Monitoring
Obfuscation and Typosquatting Checks
File Path Scanner
Network Activity Checker


Configuration
Contributing
License

Installation

Clone the repository:

bashCopy codegit clone https://github.com/yourusername/guardify.git
cd guardify

Set the Python path:

bashCopy codeexport PYTHONPATH="${PYTHONPATH}:$(pwd)"
Usage
Monitoring
To start monitoring your Python project, run the main script:
bashCopy codepython3 src/guardify/main.py
Obfuscation and Typosquatting Checks
To check for obfuscation and typosquatting issues, run the following command:
bashCopy codepython3 guardify.py pip install colurama.tar.gz
File Path Scanner
To scan for suspicious file path access, run the file path scanner:
bashCopy codepython3 filepath_scanner.py
Then, install the package:
bashCopy codepip install {package_name}
Network Activity Checker
To check for malicious network activity, first run the following command:
bashCopy codesudo strace -f -e trace=execve,connect pip install {package_name} > output.log 2>&1
Then, run the network activity checker:
bashCopy codepython3 ip_checker.py
Configuration
Guardify uses a configuration file (config/config.yaml) to customize its behavior. You can modify the following settings:

File path filters: config/filters/filepath_filters/filepaths_v1.json
Network filters: config/filters/network_filters/secured_ips.txt
Obfuscation pattern filters: config/filters/obfuscation_pattern_filters/patterns_v1.json
Typosquatting filters:

npm: config/filters/typosquat_filters/npm_suspect_names.txt
pip: config/filters/typosquat_filters/pip_suspect_names.txt



Contributing
We welcome contributions to Guardify! Please read our contribution guidelines to get started.

Author:
https://www.linkedin.com/in/rgchandrasekaraa/
