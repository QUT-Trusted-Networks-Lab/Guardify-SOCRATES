```markdown
# Guardify

Guardify is a robust Python package security tool designed to protect your Python projects from various security threats. It offers features to detect and prevent issues like obfuscation, typosquatting, suspicious file path access, and malicious network activity.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Monitoring](#monitoring)
  - [Obfuscation and Typosquatting Checks](#obfuscation-and-typosquatting-checks)
  - [File Path Scanner](#file-path-scanner)
  - [Network Activity Checker](#network-activity-checker)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/guardify.git
   cd guardify
   ```

2. **Set the Python path**:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

## Usage

### Monitoring
To start monitoring your Python project, run the main script:
```bash
python3 src/guardify/main.py
```

### Obfuscation and Typosquatting Checks
Check for obfuscation and typosquatting issues with:
```bash
python3 guardify.py pip install colurama.tar.gz
```

### File Path Scanner
Scan for suspicious file path access:
```bash
python3 filepath_scanner.py
```
Then, install the package:
```bash
pip install {package_name}
```

### Network Activity Checker
Check for malicious network activity by running:
```bash
sudo strace -f -e trace=execve,connect pip install {package_name} > output.log 2>&1
```
Then, run the network activity checker:
```bash
python3 ip_checker.py
```

## Configuration
Guardify uses a `config/config.yaml` file to customize its behavior. Modify settings in:

- **File path filters**: `config/filters/filepath_filters/filepaths_v1.json`
- **Network filters**: `config/filters/network_filters/secured_ips.txt`
- **Obfuscation pattern filters**: `config/filters/obfuscation_pattern_filters/patterns_v1.json`
- **Typosquatting filters**:
  - npm: `config/filters/typosquat_filters/npm_suspect_names.txt`
  - pip: `config/filters/typosquat_filters/pip_suspect_names.txt`

## Contributing
We welcome contributions to Guardify! Please read our [contribution guidelines](CONTRIBUTING.md) to get started.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
For more information, contact the author at [LinkedIn Profile](https://www.linkedin.com/in/rgchandrasekaraa/).
```
