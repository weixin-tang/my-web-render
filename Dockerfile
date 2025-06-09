# 使用官方 Python 运行时作为父镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 将依赖文件复制到容器中
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 将当前目录内容复制到容器的 /app 目录
COPY . .

# 暴露端口，以便 Docker 容器外可以访问应用
EXPOSE 8008

# 定义运行应用的命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008"]