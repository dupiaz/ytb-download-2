import re


def validate_youtube_url(url: str) -> bool:
    """Xác thực URL có phải là link YouTube hợp lệ hay không."""
    pattern = r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[A-Za-z0-9_-]{11}$"
    return bool(re.match(pattern, url))
