from typing import Optional

from download_flow.validate_url import detect_platform as _detect


def detect_platform(url: str) -> Optional[str]:
    """
    Nhận diện platform từ URL.
    Trả về 'youtube' hoặc 'x'. None nếu không nhận diện được.

    Ví dụ:
        detect_platform("https://youtube.com/watch?v=abc123def45")  # 'youtube'
        detect_platform("https://x.com/user/status/123456789")      # 'x'
        detect_platform("https://facebook.com/video/123")           # None
    """
    return _detect(url)
