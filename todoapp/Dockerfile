# 使用 Python 3.11 官方镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# 复制项目文件
COPY pyproject.toml uv.lock ./

# 安装依赖
RUN uv sync --frozen --no-dev

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 设置环境变量
ENV PYTHONPATH=/app
ENV UV_SYSTEM_PYTHON=1

# 启动命令
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
