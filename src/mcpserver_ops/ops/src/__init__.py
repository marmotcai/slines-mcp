class LogEntry:
    def __init__(self, timestamp, level, message):
        self.timestamp = timestamp
        self.level = level
        self.message = message

    def __repr__(self):
        return f"{self.timestamp} [{self.level}] {self.message}"

class ContainerLog:
    def __init__(self, container_name, log_entries):
        self.container_name = container_name
        self.log_entries = log_entries

    def search(self, keyword):
        return [entry for entry in self.log_entries if keyword in entry.message]