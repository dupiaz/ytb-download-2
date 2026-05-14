param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Url
)

$ServiceName = "app"

Write-Host "--- Đang kiểm tra trạng thái Docker ---" -ForegroundColor Cyan

# Kiểm tra container có đang chạy không
$Running = docker-compose ps --status running -q $ServiceName

if (-not $Running) {
    Write-Host "Container chưa chạy. Đang khởi động..." -ForegroundColor Yellow
    docker-compose up -d $ServiceName
    # Đợi một chút để container ổn định
    Start-Sleep -Seconds 2
} else {
    Write-Host "Container đã sẵn sàng." -ForegroundColor Green
}

Write-Host "--- Bắt đầu tải video ---" -ForegroundColor Cyan
docker-compose exec $ServiceName python download_flow/download_video.py $Url
