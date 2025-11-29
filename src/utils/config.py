import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def load_config():
    config_path = PROJECT_ROOT / "config.yaml"
    with open(config_path, "r") as file:
        return yaml.safe_load(file)