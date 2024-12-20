# Sử dụng Python 3.9 làm base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy source code vào container
COPY src/ /app/src/
COPY requirements.txt .

# Cài đặt dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Tạo các file __init__.py nếu chưa có
RUN touch /app/src/__init__.py \
    /app/src/bot/__init__.py \
    /app/src/utils/__init__.py

# Thiết lập PYTHONPATH
ENV PYTHONPATH=/app/src

# Expose port 8000
EXPOSE 8000

# Chạy ứng dụng
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
