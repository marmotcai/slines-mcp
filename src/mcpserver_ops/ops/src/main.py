import argparse
from ansible_utils import AnsibleUtils
from ssh_client import SSHClient
from log_fetcher import LogFetcher

def main():
    parser = argparse.ArgumentParser(description='运维工具')
    parser.add_argument('--host', required=True, help='远程服务器主机名或IP地址')
    parser.add_argument('--user', required=True, help='SSH用户名')
    parser.add_argument('--password', required=True, help='SSH密码')
    parser.add_argument('--log_type', choices=['system', 'container'], required=True, help='日志类型: system 或 container')
    parser.add_argument('--lines', type=int, default=50, help='获取日志的行数，默认为50行')
    parser.add_argument('--keyword', help='关键字搜索')

    args = parser.parse_args()

    ssh_client = SSHClient(args.host, args.user, args.password)
    log_fetcher = LogFetcher(ssh_client)

    try:
        ssh_client.connect()
        if args.log_type == 'system':
            logs = log_fetcher.fetch_system_logs(args.lines)
        else:
            logs = log_fetcher.fetch_container_logs(args.lines)

        if args.keyword:
            logs = log_fetcher.search_logs(logs, args.keyword)

        for log in logs:
            print(log)

    finally:
        ssh_client.disconnect()

if __name__ == '__main__':
    main()