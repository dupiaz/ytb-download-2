def receive_upload_confirmation(drive_link: str) -> dict:
    """Nhận xác nhận upload và link file từ Google Drive."""
    return {"status": "uploaded", "drive_link": drive_link}
