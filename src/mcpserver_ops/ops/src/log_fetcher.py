class LogFetcher:
    def __init__(self, ssh_client):
        self.ssh_client = ssh_client

    def fetch_system_logs(self, num_lines=50):
        command = f"tail -n {num_lines} /var/log/syslog"
        return self.ssh_client.execute_command(command)

    def fetch_container_logs(self, container_name, num_lines=50):
        command = f"docker logs --tail {num_lines} {container_name}"
        return self.ssh_client.execute_command(command)

    def search_logs(self, logs, keyword):
        return [line for line in logs.splitlines() if keyword in line]

    def save_logs_to_file(self, logs, file_path):
        with open(file_path, 'w') as file:
            file.write(logs)