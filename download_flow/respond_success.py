def respond_success(drive_link: str) -> dict:
    """Tạo phản hồi thành công cho UI cùng link Google Drive."""
    return {
        "success": True,
        "message": "Video đã được tải lên Google Drive thành công.",
        "drive_link": drive_link
    }
