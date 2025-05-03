import yaml
import os
from dotenv import load_dotenv


load_dotenv()

def load_config(config_path="config.yaml"):
    """Loads the YAML configuration file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def get_api_key(provider_key_name: str):
    """Gets API key from environment variables."""
    key = os.getenv(provider_key_name)
    if not key:
        raise ValueError(f"API Key '{provider_key_name}' not found in environment variables.")
    return key


CONFIG = load_config()


OPENAI_API_KEY = get_api_key("OPENAI_API_KEY") if CONFIG['llm']['provider'] == 'openai' else None
