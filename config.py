import json
import atexit
import os
from loguru import logger
from config import config
import sys

logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", level=config.log_level)

class Config:
    CONFIG_FILE = "config.json"

    def __init__(self):
        self.zoom_level = 1
        self.window_x = 800
        self.window_y = 600
        self.log_level = "INFO"
        self.load_config()
        atexit.register(self.save_config)

    def load_config(self):
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.__dict__.update(data)
        except Exception as e:
            logger.error(f"Error loading config: {e}")

    def save_config(self):
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(self.__dict__, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving config: {e}")

config = Config()