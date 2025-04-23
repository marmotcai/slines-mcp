ARG BASE_IMAGE=python:3.10-slim
FROM ${BASE_IMAGE} AS base

LABEL maintainer="marmotcai@163.com"

#######################################################

RUN sed -i 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources
RUN apt-get update && apt-get install -y \
    procps iputils-ping net-tools vim git

#######################################################

ENV PIP_MIRRORS_URL="https://pypi.tuna.tsinghua.edu.cn/simple"
    
RUN pip config set global.index-url ${PIP_MIRRORS_URL}
RUN python -m pip install --upgrade pip && \
    pip install uv

RUN uv venv /root/.venv && echo '. /root/.venv/bin/activate' >> ~/.bashrc

# Install project Python dependencies
# COPY requirements.txt .
# RUN pip install -r requirements.txt

#################################################################################

FROM base AS dev

ARG APP_NAME=
WORKDIR /app

# Copy source code into container
COPY ./src/${APP_NAME}/ .
RUN . /root/.venv/bin/activate && \
    uv pip install -r requirements.txt

COPY ./src/entrypoint.sh /root/entrypoint.sh

CMD ["bash", "/root/entrypoint.sh"]
