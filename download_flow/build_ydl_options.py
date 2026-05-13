import os


# Cấu hình format theo từng platform
_PLATFORM_FORMAT: dict[str, str] = {
    # YouTube: ưu tiên VP9/m4a riêng rồi merge; fallback về best mp4
    "youtube": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    # X.com: thường encode sẵn H.264 trong 1 stream mp4 — ưu tiên native mp4
    "x": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best",
}

_DEFAULT_COOKIES_PATH = "/app/cookies.txt"


def _is_valid_cookies_file(path: str) -> bool:
    """
    Kiểm tra file cookies có đúng định dạng Netscape HTTP Cookie File không.
    yt-dlp yêu cầu dòng đầu tiên không phải comment phải là header chuẩn.
    Trả về False nếu file không tồn tại, rỗng, hoặc chỉ chứa comments.
    """
    if not path or not os.path.isfile(path) or os.path.getsize(path) == 0:
        return False
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped.startswith("#"):
                    # Header Netscape hợp lệ: "# Netscape HTTP Cookie File"
                    if "Netscape HTTP Cookie File" in stripped:
                        return True
                    continue
                # Dòng data đầu tiên không phải comment → có thể là cookie thực
                return True
    except OSError:
        return False
    return False


def build_ydl_options(
    platform: str,
    output_template: str,
    cookies_path: str = _DEFAULT_COOKIES_PATH,
) -> dict:
    """
    Tạo dict ydl_opts cho yt-dlp dựa theo platform và cookies.

    Args:
        platform:        'youtube' hoặc 'x'
        output_template: chuỗi outtmpl của yt-dlp
        cookies_path:    đường dẫn tới cookies.txt (bypass xác thực X.com)

    Returns:
        dict sẵn sàng truyền vào YoutubeDL(opts)
    """
    opts: dict = {
        "outtmpl": output_template,
        "format": _PLATFORM_FORMAT.get(platform, "best"),
        "merge_output_format": "mp4",
        "ffmpeg_location": "/usr/bin/ffmpeg",
        "quiet": False,
        "noplaylist": True,
    }

    # Cookie logic tập trung tại đây
    # Chỉ inject khi file tồn tại VÀ đúng định dạng Netscape
    if _is_valid_cookies_file(cookies_path):
        opts["cookiefile"] = cookies_path
    else:
        if cookies_path and os.path.isfile(cookies_path):
            print(f"[build_ydl_options] cookies.txt không đúng định dạng Netscape — bỏ qua.")

    return opts

