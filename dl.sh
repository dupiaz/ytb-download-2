#!/bin/bash

# Kiểm tra nếu không có URL truyền vào
if [ -z "$1" ]; then
    echo "Sử dụng: ./dl.sh <URL>"
    echo "Ví dụ: ./dl.sh https://x.com/user/status/123"
    exit 1
fi

URL=$1
SERVICE_NAME="app"

echo "--- Đang kiểm tra trạng thái Docker ---"

# Kiểm tra container có đang chạy không
RUNNING=$(docker-compose ps --status running -q $SERVICE_NAME)

if [ -z "$RUNNING" ]; then
    echo "Container chưa chạy. Đang khởi động..."
    docker-compose up -d $SERVICE_NAME
    # Đợi một chút để container ổn định
    sleep 2
else
    echo "Container đã sẵn sàng."
fi

echo "--- Bắt đầu tải video ---"
docker-compose exec $SERVICE_NAME python download_flow/download_video.py "$URL"
