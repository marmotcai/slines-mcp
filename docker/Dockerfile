ARG BASE_IMAGE=python:3.10-slim
FROM ${BASE_IMAGE}

LABEL maintainer="marmotcai@163.com"

# Set working directory
WORKDIR /app

#######################################################

RUN sed -i 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources
RUN apt-get update && apt-get install -y \
    procps iputils-ping net-tools vim git

#######################################################

ENV PIP_MIRRORS_URL="https://pypi.tuna.tsinghua.edu.cn/simple"
    
RUN pip config set global.index-url ${PIP_MIRRORS_URL}
RUN python -m pip install --upgrade pip && \
    pip install uv

# Install MCP SDK directly from GitHub repository
# RUN pip install git+https://github.com/modelcontextprotocol/python-sdk.git

# Install project Python dependencies
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# Copy source code into container
COPY . .
RUN uv venv /root/.venv && echo '. /root/.venv/bin/activate' >> ~/.bashrc
RUN . /root/.venv/bin/activate && \
    uv pip install -r requirements.txt
# RUN uv pip install -e .

CMD ["bash", "entrypoint.sh"]
