# YouTube Download Project - Codebase Context

## 📋 Project Overview
YouTube/X.com video downloader with Google Drive integration (60% complete)
- **Purpose:** Download videos from YouTube or X.com (Twitter), upload to Google Drive
- **Status:** Core download working; Drive upload & metadata fetching still TODO
- **Tech Stack:** Python 3.12, yt-dlp, FFmpeg, Docker, pytest

---

## 🏗️ Architecture

**Data Pipeline:**
```
URL → Validate → Detect Platform → Build Config → Download Video → Save File → Upload Drive → Response
```

**Component Organization:**
- Core modules in `download_flow/` (functional architecture)
- Deploy via Docker (Windows: `dl.ps1`, Unix: `dl.sh`)
- Tests in `tests/test_new_modules.py`

---

## 📁 Key Files Reference

### Core Download Flow (`download_flow/`)
| File | Purpose |
|------|---------|
| `download_video.py` | **Main entry** - orchestrates download, calls yt-dlp, normalizes filename |
| `validate_url.py` | URL regex validation + platform detection (returns 'youtube' or 'x') |
| `detect_platform.py` | Platform detection wrapper |
| `build_ydl_options.py` | Builds yt-dlp options dict per platform; validates cookies.txt |
| `upload_to_google_drive.py` | TODO: Google Drive upload stub |
| `respond_success.py` | Return `{"success": true, "message": ..., "drive_link": ...}` |
| `respond_invalid_url_error.py` | Return error response |

### Deployment
| File | Purpose |
|------|---------|
| `Dockerfile` | Python 3.12 + ffmpeg + latest yt-dlp; working dir `/app` |
| `docker-compose.yml` | Service config; mounts project & cookies.txt; port 8000 |
| `dl.ps1` / `dl.sh` | Start Docker container, run download inside |

### Output
- **Download location:** `video_2/{title}-{id}.mp4`
- **Filename format:** Normalized (spaces→hyphens, special chars removed)

---

## 🔄 Data Flow

1. **URL Input** → `dl.sh "https://youtube.com/watch?v=..."`
2. **Validation** → Regex match (YouTube: 11-char ID; X.com: status pattern)
3. **Platform Detection** → Returns `'youtube'` or `'x'`
4. **Config Building** →
   - YouTube: `"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"`
   - X.com: `"bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best"`
   - Load cookies.txt if valid (Netscape format)
5. **Download** → yt-dlp extracts + FFmpeg merges audio/video
6. **Save** → Outputs to `video_2/{title}-{id}.mp4`
7. **Response** → Success message with file path (Drive upload TODO)

---

## 🧪 Testing

**Framework:** pytest  
**Test file:** `tests/test_new_modules.py` (~150 lines)

**Coverage:**
- URL validation (YouTube, X.com, invalid patterns)
- Platform detection (correct mapping, unknown fallback)
- yt-dlp options building (format per platform, cookies injection, fallback)
- Function signatures

**Run:** `docker compose run --rm app python -m pytest tests/test_new_modules.py -v`

---

## 🔑 Key Implementation Details

**URL Patterns:**
- YouTube: `youtube.com/watch?v={11-char-ID}` or `youtu.be/{ID}`
- X.com: `x.com/{user}/status/{ID}` or legacy `twitter.com`

**Cookies:**
- Optional Netscape format file for X.com authentication
- Validates: file exists, has header, non-empty
- Gracefully skips if invalid (download may fail for private videos)

**Docker Workflow:**
1. Check if container `ytb-download-app` running
2. If not, start with `docker-compose up -d app`
3. Wait 2s for stability
4. Execute download inside container
5. Container persists (faster subsequent runs)

---

## ✅ Production-Ready vs TODO

**✅ Complete:**
- URL validation & platform detection (fully tested)
- yt-dlp config (platform-aware, cookies-aware)
- Docker containerization
- Video download & filename normalization
- Test suite

**⏳ TODO:**
- Google Drive upload (stub: `upload_to_google_drive.py`)
- Metadata fetching (stub: `fetch_youtube_video.py`)
- Request/response API layer (UI integration stubs)

---

## 💡 Quick Reference for Agents

- **Main entry point:** `download_flow/download_video.py::download_to_drive_folder()`
- **Platform enum:** `'youtube'` or `'x'` (from `validate_url.detect_platform()`)
- **yt-dlp options:** Built by `build_ydl_options(platform, cookies_path=None)` → dict
- **Response format:** Dict with keys `success`, `message`, optionally `drive_link`
- **Error handling:** Return via `respond_invalid_url_error()` (no exceptions thrown)
- **Docker command:** `./dl.sh <URL>` or `./dl.ps1 <URL>`
