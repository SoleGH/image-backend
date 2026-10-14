FROM python:3.12-slim

#RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources
#RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list
# Debian 12 后使用sources.list.d/debian.sources 替换了 sources.list
RUN sed -i 's|https://deb.debian.org|https://mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's|http://security.debian.org|https://mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources
#ENV ENVIRONMENT=production
RUN uname
# 解决mysqlclient 依赖 使用pymysql 取代mysqlclient 不需要依赖
#RUN apt-get update && apt-get install -y libgl1 default-libmysqlclient-dev \
#    pkg-config \
#    gcc \
#    g++ \
#    python3-dev
#ADD ./src /src
COPY ./src/requirements /src/
WORKDIR /src

RUN pip install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
RUN pip install -r requirements -i  http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com