FROM python:3.9-slim-buster

# 替换 apt 源为清华（两种架构通用）
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i '/buster-updates/d' /etc/apt/sources.list

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    ca-certificates \
    build-essential \
    python3-dev \
    libcairo2-dev \
    libgirepository1.0-dev \
    gir1.2-appindicator3-0.1 \
    python3-pil \
    python3-xlib \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# 安装 Node.js 24 (自动适配架构)
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*