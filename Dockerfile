# 使用 Python 3.12 (Debian bookworm) 镜像作为基础镜像
FROM python:3.12-slim-bookworm

WORKDIR /app
ENV TZ=Asia/Shanghai

RUN pip install --no-cache-dir qbittorrent-api
# 更新 apt 包并安装 cron 和其他依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata vim && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY main.py crontablist entrypoint.sh  /app
RUN  crontab crontablist && mkdir -p /log && echo "alias ll='ls -l'" >> /root/.bashrc

# 启动 cron 服务
CMD ["/app/entrypoint.sh"]
