# 使用官方 Python 映像檔作為基礎映像檔
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 將當前目錄下的所有文件複製到工作目錄
COPY . /app

# 安裝 Flask 和其他依賴庫
RUN pip install --no-cache-dir -r requirements.txt

# 開放應用程式所需的端口號
EXPOSE 5000

# 執行應用程式
CMD ["python", "app.py"]
