#!/bin/bash

# 定义帮助信息函数
print_help() {
  echo "使用方法: $0 [-a] [-s [build|push]]"
  echo "选项："
  echo "  -s    构建服务"
  echo "        - build: 构建并运行容器"
  echo "        - push: 推送容器"
  echo "        - up: 运行容器"
  echo "  -t    安装工具"
  echo "        - docker-compose: 安装 docker-compose"
  exit 1
}

# 获取完整的命令行
MAIN_DIR=$(dirname "$(readlink -f "$0")")
base_env_file="${MAIN_DIR}/.env"

os_type=$(uname)
if [[ -f /etc/unraid-version ]]; then
  echo "Running on unRAID"
  base_env_file="${MAIN_DIR}/.env_unraid"
elif [[ "$os_type" == "Darwin" ]]; then
  echo "Running on macOS"
  base_env_file="${MAIN_DIR}/.env_mac"
elif [[ "$os_type" == "Linux" ]]; then
  echo "Running on Linux"
  base_env_file="${MAIN_DIR}/.env_linux"
else
  echo "Unsupported OS: $os_type"
  exit 1
fi

echo ${base_env_file}

if [ -f ${base_env_file} ]; then
  source ${base_env_file}
fi

# 如果没有参数，显示帮助信息
if [ $# -eq 0 ]; then
  print_help
fi

while getopts "s:t:h" opt; do
  case $opt in
  s)
    action="$OPTARG"
    
    case "$action" in
      push)
        # 使用 while 循环代替 xargs
        CMD='docker images --format "{{.Repository}}:{{.Tag}}" | grep "${IMAGE_REGISTRY_NAME}" | while read img; do docker push "$img"; done'
        ;;

      build|up|upd|down|restart)
        shift $((OPTIND-1))
        profile="${1:-}"  # 允许服务名为空
        if [ -z "$profile" ]; then
            profile=${DEFAULT_PROFILE}
        fi

        # 动态构建命令
        base_cmd="docker-compose --env-file ${base_env_file} --profile $profile -f ./docker-compost.yaml"
        [ "$action" = "build" ] && base_cmd+=" --project-directory ${MAIN_DIR} up --build"
        [ "$action" = "up" ] && base_cmd+=" up"
        [ "$action" = "upd" ] && base_cmd+=" up -d"
        [ "$action" = "down" ] && base_cmd+=" down"
        [ "$action" = "restart" ] && base_cmd+=" restart"

        CMD="$base_cmd"
        ;;

      *)
        echo "未知的操作: $action"
        print_help
        ;;
    esac
    ;;

  t)
    # 使用逗号分隔多个参数
    IFS=',' read -ra params <<< "$OPTARG"
    param1=${params[0]}
    param2=${params[1]}
    param3=${params[2]}

    if [ "$param1" = "docker-compose" ]; then
      # export HTTPS_PROXY=proxy.atoml.net:30090
      curl -L https://github.com/docker/compose/releases/download/v2.29.5/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
      chmod +x /usr/local/bin/docker-compose    
    fi

    ;;    

  h)
    print_help
    ;;

  \?)
    echo "错误: 无效的选项 -$OPTARG" >&2
    print_help
    ;;
  esac
done

if [ -n "$CMD" ]; then
  echo "执行命令: $CMD"
  eval "$CMD"
fi