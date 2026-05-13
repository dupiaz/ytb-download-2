import sys
from pathlib import Path

from yt_dlp import YoutubeDL


def download_to_drive_folder(url: str, output_dir: Path, ydl_opts: dict) -> Path:
    """
    Tải video từ URL (YouTube hoặc X.com) vào output_dir.

    Args:
        url:       URL video (YouTube hoặc X.com/Twitter)
        output_dir: Thư mục lưu file tải về
        ydl_opts:  Dict cấu hình yt-dlp — tạo bằng build_ydl_options()
                   (Breaking change từ v1.1: không còn hardcode bên trong hàm này)

    Returns:
        Path tới file .mp4 đã tải về và đổi tên
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(output_dir / "%(title)s-%(id)s.%(ext)s")

    # Ghi đè outtmpl để dùng output_dir được truyền vào
    opts = {**ydl_opts, "outtmpl": output_template}

    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)

    filename = Path(ydl.prepare_filename(info))
    if filename.suffix != ".mp4":
        filename = filename.with_suffix(".mp4")

    # Normalize filename: bỏ ký tự đặc biệt và khoảng trắng
    new_name = filename.name.replace(" ", "-").replace("⧸", "").replace("/", "-")
    new_filename = filename.parent / new_name
    if filename != new_filename:
        filename.rename(new_filename)
        filename = new_filename

    return filename


if __name__ == "__main__":
    import os as _os
    # Thêm thư mục gốc project vào sys.path để import download_flow hoạt động
    _project_root = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
    if _project_root not in sys.path:
        sys.path.insert(0, _project_root)

    from download_flow.build_ydl_options import build_ydl_options
    from download_flow.detect_platform import detect_platform

    if len(sys.argv) < 2:
        print("Usage: python download_flow/download_video.py <url>")
        sys.exit(1)

    input_url = sys.argv[1]
    platform = detect_platform(input_url) or "youtube"
    print(f"Platform detected: {platform}")
    opts = build_ydl_options(platform, output_template="video_2/%(title)s-%(id)s.%(ext)s")
    output_path = download_to_drive_folder(input_url, Path("video_2"), opts)
    print(f"Downloaded video to: {output_path}")

