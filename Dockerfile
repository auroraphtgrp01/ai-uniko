# Sử dụng Python 3.9 làm base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các dependencies cần thiết
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt trước để tận dụng cache của Docker
COPY requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . /app/

# Tạo các file __init__.py nếu chưa có
RUN mkdir -p /app/src/bot /app/src/utils \
    && touch /app/src/__init__.py /app/src/bot/__init__.py /app/src/utils/__init__.py

# Thiết lập biến môi trường
ENV PYTHONPATH=/app \
    PYTHON_PATH=/app \
    PYTHONUNBUFFERED=1

# Expose port mà FastAPI sẽ chạy
EXPOSE 8000

# Debug: Liệt kê các files và thư mục
RUN echo "=== Listing /app ===" && \
    ls -la /app && \
    echo "=== Listing /app/src ===" && \
    ls -la /app/src && \
    echo "=== Listing /app/src/bot ===" && \
    ls -la /app/src/bot && \
    echo "=== Python path ===" && \
    python -c "import sys; print('\n'.join(sys.path))" && \
    echo "=== Current directory ===" && \
    pwd

# Command để chạy ứng dụng
CMD ["python", "-m", "uvicorn", "--app-dir", "/app", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
