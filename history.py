import json
import os

class History:
    def __init__(self):
        self.history = []
        self.backup_file = "history.json.bak"

    def add(self, data):
        self.history.append(data)
        self._backup()

    def get(self):
        return self.history

    def _backup(self):
        try:
            with open(self.backup_file, 'w') as f:
                json.dump(self.history, f)
        except Exception as e:
            print(f"Failed to backup history: {e}")

    def restore_backup(self):
        try:
            if os.path.exists(self.backup_file):
                with open(self.backup_file, 'r') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Failed to restore history: {e}")
            self.history = []