import os
import yaml
import json
from yaml.parser import ParserError
from yaml.scanner import ScannerError

class ConfigLoaderError(Exception):
    pass

class ConfigLoader:
    def __init__(self, config_path='config/config.yaml'):
        self.config_path = config_path
        self.config = {}

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise ConfigLoaderError(f"Configuration file {self.config_path} not found.")

        try:
            with open(self.config_path, 'r') as file:
                self.config = yaml.safe_load(file) or {}
        except (ParserError, ScannerError) as e:
            raise ConfigLoaderError(f"Error parsing YAML configuration: {e}")
        except Exception as e:
            raise ConfigLoaderError(f"An unknown error occurred while loading the configuration: {e}")

        self._load_plugin_configs()
        self._validate_config()
        return self.config

    def _load_plugin_configs(self):
        for plugin_key, plugin_config in self.config.get('plugins', {}).items():
            if 'paths_config_file' in plugin_config:
                paths_config_file = plugin_config['paths_config_file']
                plugin_config['monitored_paths'] = self._load_paths_from_file(paths_config_file)

            if 'ignored_ips_file' in plugin_config:
                ignored_ips_file = plugin_config['ignored_ips_file']
                plugin_config['ignored_ips'] = self._load_ips_from_file(ignored_ips_file)
            

    def _load_paths_from_file(self, file_path):
        if not os.path.exists(file_path):
            raise ConfigLoaderError(f"File {file_path} not found.")
        with open(file_path, 'r') as file:
            return file.read().splitlines()

    def _load_ips_from_file(self, file_path):
        if not os.path.exists(file_path):
            raise ConfigLoaderError(f"File {file_path} not found.")
        with open(file_path, 'r') as file:
            return [ip.strip() for ip in file if ip.strip()]

    def _validate_config(self):
        if 'global' not in self.config:
            raise ConfigLoaderError("Global settings are missing in the configuration.")

# Usage
if __name__ == "__main__":
    try:
        loader = ConfigLoader()
        config = loader.load_config()
        print(config)  # Prints the loaded configuration for debugging purposes
    except ConfigLoaderError as e:
        print(f"Configuration error: {e}")
