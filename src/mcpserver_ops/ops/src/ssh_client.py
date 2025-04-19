class SSHClient:
    def __init__(self, hostname, port=22, username=None, password=None, key_file=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_file = key_file
        self.client = None
        self.sftp = None

    def connect(self):
        import paramiko
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if self.key_file:
            self.client.connect(self.hostname, port=self.port, username=self.username, key_filename=self.key_file)
        else:
            self.client.connect(self.hostname, port=self.port, username=self.username, password=self.password)

    def execute_command(self, command):
        if not self.client:
            raise Exception("SSH client is not connected.")
        
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.readlines(), stderr.readlines()

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None