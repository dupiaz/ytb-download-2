import re
from typing import Optional


# Regex patterns cho từng platform được hỗ trợ
PATTERNS: dict[str, str] = {
    "youtube": r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[A-Za-z0-9_-]{11}",
    "x":       r"^(https?://)?(www\.)?(x|twitter)\.com/\w+/status/\d+(\?.*)?$",
}


def validate_url(url: str) -> bool:
    """Trả về True nếu URL thuộc YouTube hoặc X.com (Twitter)."""
    return any(re.match(pattern, url) for pattern in PATTERNS.values())


def detect_platform(url: str) -> Optional[str]:
    """
    Nhận diện platform từ URL.
    Trả về 'youtube' hoặc 'x'. None nếu không nhận diện được.
    """
    for platform, pattern in PATTERNS.items():
        if re.match(pattern, url):
            return platform
    return None
