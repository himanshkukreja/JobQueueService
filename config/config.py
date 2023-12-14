import os
import yaml
from logger.logging import get_logger

logger = get_logger(__name__)
cwd = os.getcwd()

def load_yaml_config(filename):
    with open(filename, "r") as file:
        content = yaml.safe_load(file)
        return content if content else {}

# List of application.yaml files
config_files = [
    os.path.join(cwd, "config", "application.yaml")
]

# Merge configurations from each file
config = {}
for file in config_files:
    if os.path.exists(file):
        config_content = load_yaml_config(file)
        if config_content:
            config.update(config_content)
        else:
            logger.warning(f"Config file {file} is empty or improperly formatted.")
    else:
        logger.warning(f"Config file {file} not found.")
    




max_attempts = config["max_attempts"]
max_delay = config["max_delay"]
processing_system_endpoint = config["processing_system_endpoint"]
sqs_url= config["sqs_url"]