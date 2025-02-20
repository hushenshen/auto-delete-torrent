# 使用 Python 3.8.10 镜像作为基础镜像
FROM python:3.8.10

WORKDIR /app
ENV TZ=Asia/Shanghai

RUN pip install --no-cache-dir qbittorrent-api
# 更新 apt 包并安装 cron 和其他依赖
RUN apt-get update && \
    apt-get install -y cron && \
    apt-get install -y bash && \
    apt-get install -y tzdata && \
    apt-get install -y vim && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean 


COPY main.py crontablist entrypoint.sh  /app
RUN  crontab crontablist && mkdir -p /log && echo "alias ll='ls -l'" >> ~/.bashrc

# 启动 cron 服务
CMD ["/app/entrypoint.sh"]
