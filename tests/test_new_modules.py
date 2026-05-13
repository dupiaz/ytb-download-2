"""
Unit tests cho các module mới:
  - validate_url.py
  - detect_platform.py
  - build_ydl_options.py
  - download_video.py (signature mới)

Chạy trong Docker:
  docker compose run --rm app python -m pytest tests/test_new_modules.py -v
"""
import sys
import os

# Đảm bảo import từ thư mục gốc project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from download_flow.validate_url import validate_url, detect_platform
from download_flow.build_ydl_options import build_ydl_options


# ---------------------------------------------------------------------------
# Group 1: validate_url()
# ---------------------------------------------------------------------------
class TestValidateUrl:

    # --- YouTube URLs hợp lệ ---
    @pytest.mark.parametrize("url", [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
        "http://youtu.be/dQw4w9WgXcQ",
        "youtu.be/dQw4w9WgXcQ",
    ])
    def test_valid_youtube_urls(self, url):
        assert validate_url(url) is True, f"Expected True for YouTube URL: {url}"

    # --- X.com URLs hợp lệ ---
    @pytest.mark.parametrize("url", [
        "https://x.com/elonmusk/status/1234567890123456789",
        "https://www.x.com/user123/status/9876543210",
        "https://twitter.com/user/status/111222333444",
        "http://twitter.com/username/status/999?s=20",
    ])
    def test_valid_x_urls(self, url):
        assert validate_url(url) is True, f"Expected True for X URL: {url}"

    # --- URLs không hợp lệ ---
    @pytest.mark.parametrize("url", [
        "https://facebook.com/video/123",
        "https://tiktok.com/@user/video/123",
        "not-a-url",
        "",
        "https://x.com/user",               # Thiếu /status/ID
        "https://youtube.com/channel/ABC",   # Không phải video URL
    ])
    def test_invalid_urls(self, url):
        assert validate_url(url) is False, f"Expected False for: {url}"


# ---------------------------------------------------------------------------
# Group 2: detect_platform()
# ---------------------------------------------------------------------------
class TestDetectPlatform:

    @pytest.mark.parametrize("url, expected", [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "youtube"),
        ("https://youtu.be/dQw4w9WgXcQ",               "youtube"),
        ("https://x.com/user/status/123456789",         "x"),
        ("https://twitter.com/user/status/123456789",   "x"),
    ])
    def test_detect_known_platforms(self, url, expected):
        result = detect_platform(url)
        assert result == expected, f"URL '{url}': got '{result}', expected '{expected}'"

    @pytest.mark.parametrize("url", [
        "https://facebook.com/video/123",
        "not-a-url",
        "",
    ])
    def test_detect_unknown_returns_none(self, url):
        result = detect_platform(url)
        assert result is None, f"Expected None for unknown URL: {url}"


# ---------------------------------------------------------------------------
# Group 3: build_ydl_options()
# ---------------------------------------------------------------------------
class TestBuildYdlOptions:

    def test_youtube_format_in_opts(self):
        opts = build_ydl_options("youtube", "output/%(title)s.%(ext)s")
        assert "bestvideo" in opts["format"]
        assert opts["merge_output_format"] == "mp4"
        assert opts["noplaylist"] is True

    def test_x_format_in_opts(self):
        opts = build_ydl_options("x", "output/%(title)s.%(ext)s")
        assert "bv*" in opts["format"] or "best" in opts["format"]
        assert opts["merge_output_format"] == "mp4"

    def test_no_cookiefile_when_path_missing(self):
        opts = build_ydl_options("x", "output/%(title)s.%(ext)s",
                                 cookies_path="/nonexistent/cookies.txt")
        assert "cookiefile" not in opts

    def test_no_cookiefile_when_path_is_none(self):
        opts = build_ydl_options("youtube", "output/%(title)s.%(ext)s",
                                 cookies_path=None)
        assert "cookiefile" not in opts

    def test_cookiefile_injected_when_valid(self, tmp_path):
        # Tạo file cookies giả có nội dung
        fake_cookies = tmp_path / "cookies.txt"
        fake_cookies.write_text("# Netscape HTTP Cookie File\n")
        opts = build_ydl_options("x", "output/%(title)s.%(ext)s",
                                 cookies_path=str(fake_cookies))
        assert "cookiefile" in opts
        assert opts["cookiefile"] == str(fake_cookies)

    def test_cookiefile_not_injected_when_empty(self, tmp_path):
        # File tồn tại nhưng rỗng
        empty_cookies = tmp_path / "cookies.txt"
        empty_cookies.write_text("")
        opts = build_ydl_options("x", "output/%(title)s.%(ext)s",
                                 cookies_path=str(empty_cookies))
        assert "cookiefile" not in opts

    def test_unknown_platform_uses_best_fallback(self):
        opts = build_ydl_options("instagram", "output/%(title)s.%(ext)s")
        assert opts["format"] == "best"

    def test_outtmpl_is_overridable(self):
        template = "custom/path/%(id)s.%(ext)s"
        opts = build_ydl_options("youtube", template)
        assert opts["outtmpl"] == template


# ---------------------------------------------------------------------------
# Group 4: download_video.py — kiểm tra signature mới (không thực sự download)
# ---------------------------------------------------------------------------
class TestDownloadVideoSignature:

    def test_function_accepts_ydl_opts_param(self):
        """Kiểm tra hàm có tham số ydl_opts — không cần thực sự chạy download."""
        import inspect
        from download_flow.download_video import download_to_drive_folder
        sig = inspect.signature(download_to_drive_folder)
        params = list(sig.parameters.keys())
        assert "url" in params
        assert "output_dir" in params
        assert "ydl_opts" in params, (
            "BREAKING CHANGE: 'ydl_opts' param không tìm thấy trong download_to_drive_folder()"
        )
