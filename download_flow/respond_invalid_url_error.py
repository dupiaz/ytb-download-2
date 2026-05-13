def respond_invalid_url_error() -> dict:
    """Tạo phản hồi lỗi khi URL không thuộc platform nào được hỗ trợ."""
    return {
        "success": False,
        "message": (
            "URL không hợp lệ hoặc không được hỗ trợ. "
            "Vui lòng kiểm tra lại. "
            "Các nền tảng hỗ trợ: YouTube (youtube.com, youtu.be), "
            "X / Twitter (x.com, twitter.com)."
        ),
    }

