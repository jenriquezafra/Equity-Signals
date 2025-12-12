import yaml
from pathlib import Path

# resolve absolute project path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

#standard directories
DATA_DIR = PROJECT_ROOT / "data"
FEATURES_DIR = PROJECT_ROOT / "features"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"


def load_config():
    '''
    Return full configuration from config.yaml as a Python dict
    '''
    config_path = PROJECT_ROOT / "config.yaml"
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
    
# optional convenience function
def get(key_path, default=True):
    '''
    Access nested config keys with a dotted path:
    get("data.tickers") -> list of tickers
    '''
    cfg = load_config()
    keys = key_path.split(".")
    for k in keys:
        cfg = cfg.get(k, {})
    return cfg or default
