# 使用官方 Python 3.11 基础镜像
FROM python:3.11

# 设置工作目录
WORKDIR /app

# 复制应用所需的文件到容器
COPY . /app

# 安装应用所需的依赖
RUN pip install --no-cache-dir -r requirements.txt

# 运行 init.py 来初始化数据库
RUN python init_db.py

# 暴露端口
EXPOSE 8000

# 定义容器启动时执行的命令
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:app"]
