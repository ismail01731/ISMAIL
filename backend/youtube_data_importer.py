import os
import re
import urllib.parse
import urllib.request
import json
try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None
from backend.youtube_growth import save_channel, save_video
DEFAULT_CHANNEL_ID = "UCP75FPRq4DaMoe88G9R3heg"
def _load_environment():
    env_path = r"D:\ISMAIL\config\.env"
    if load_dotenv is not None:
        try:
            load_dotenv(env_path, override=False)
        except Exception:
            pass
    existing_key = os.getenv("YOUTUBE_API_KEY", "").strip()
    if existing_key:
        return existing_key
    if not os.path.exists(env_path):
        return ""
    try:
        with open(env_path, "r", encoding="utf-8-sig") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[7:].strip()
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key.strip() != "YOUTUBE_API_KEY":
                    continue
                value = value.strip()
                if (
                    len(value) >= 2
                    and value[0] == value[-1]
                    and value[0] in ("'", '"')
                ):
                    value = value[1:-1]
                return value.strip()
    except Exception:
        return ""
    return ""
def _youtube_api(endpoint: str, params: dict) -> dict:
    api_key = _load_environment()
    if not api_key:
        raise RuntimeError(
            "YOUTUBE_API_KEY_NOT_SET: Add YOUTUBE_API_KEY to D:\\ISMAIL\\config\\.env"
        )
    params = dict(params)
    params["key"] = api_key
    url = (
        "https://www.googleapis.com/youtube/v3/"
        + endpoint
        + "?"
        + urllib.parse.urlencode(params)
    )
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ISMAIL-AI-YouTube-Importer/1.0"
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except Exception as exc:
        raise RuntimeError(f"YouTube API request failed: {exc}") from exc
def _parse_duration(value: str) -> float:
    if not value:
        return 0.0
    match = re.fullmatch(
        r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?",
        value,
    )
    if not match:
        return 0.0
    hours = float(match.group(1) or 0)
    minutes = float(match.group(2) or 0)
    seconds = float(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds
def _video_format(duration_seconds: float) -> str:
    if duration_seconds <= 60:
        return "shorts"
    return "long"
def get_channel_data(channel_id: str = DEFAULT_CHANNEL_ID) -> dict:
    result = _youtube_api(
        "channels",
        {
            "part": "snippet,contentDetails,statistics",
            "id": channel_id,
        },
    )
    items = result.get("items") or []
    if not items:
        raise RuntimeError(
            f"YouTube channel not found: {channel_id}"
        )
    return items[0]
def import_channel(
    channel_id: str = DEFAULT_CHANNEL_ID,
    max_videos: int = 50,
) -> dict:
    if max_videos < 1:
        max_videos = 1
    channel = get_channel_data(channel_id)
    snippet = channel.get("snippet") or {}
    statistics = channel.get("statistics") or {}
    content_details = channel.get("contentDetails") or {}
    uploads_playlist_id = (
        content_details
        .get("relatedPlaylists", {})
        .get("uploads")
    )
    if not uploads_playlist_id:
        raise RuntimeError(
            "YouTube uploads playlist was not found."
        )
    channel_name = snippet.get("title") or "The Ismail Jr"
    subscriber_count = int(
        statistics.get("subscriberCount", 0) or 0
    )
    video_count = int(
        statistics.get("videoCount", 0) or 0
    )
    view_count = int(
        statistics.get("viewCount", 0) or 0
    )
    save_channel(
        channel_id=channel_id,
        channel_name=channel_name,
        handle="@TheIsmailJr",
        niche="Village Vlogs, Comedy, Family & Challenges",
        language="bn",
        country="BD",
        subscriber_count=subscriber_count,
        video_count=video_count,
        view_count=view_count,
    )
    imported = 0
    pages = 0
    next_page_token = None
    while imported < max_videos:
        remaining = min(50, max_videos - imported)
        params = {
            "part": "snippet,contentDetails",
            "playlistId": uploads_playlist_id,
            "maxResults": remaining,
        }
        if next_page_token:
            params["pageToken"] = next_page_token
        page = _youtube_api("playlistItems", params)
        pages += 1
        playlist_items = page.get("items") or []
        video_ids = []
        for item in playlist_items:
            content = item.get("contentDetails") or {}
            video_id = content.get("videoId")
            if video_id:
                video_ids.append(video_id)
        if not video_ids:
            break
        videos_response = _youtube_api(
            "videos",
            {
                "part": "snippet,contentDetails,statistics",
                "id": ",".join(video_ids),
            },
        )
        for video in videos_response.get("items") or []:
            video_id = video.get("id")
            video_snippet = video.get("snippet") or {}
            video_details = video.get("contentDetails") or {}
            video_stats = video.get("statistics") or {}
            title = video_snippet.get("title") or "Untitled"
            description = video_snippet.get("description") or ""
            published_at = video_snippet.get("publishedAt")
            duration_seconds = _parse_duration(
                video_details.get("duration", "")
            )
            views = int(video_stats.get("viewCount", 0) or 0)
            likes = int(video_stats.get("likeCount", 0) or 0)
            comments = int(video_stats.get("commentCount", 0) or 0)
            tags = video_snippet.get("tags") or []
            topic = (
                tags[0]
                if tags
                else "Bangla Comedy / Village Content"
            )
            save_video(
                youtube_video_id=video_id,
                title=title,
                channel_id=channel_id,
                description=description,
                topic=topic,
                format=_video_format(duration_seconds),
                duration_seconds=duration_seconds,
                published_at=published_at,
                views=views,
                likes=likes,
                comments=comments,
                shares=0,
                subscribers_gained=0,
                impressions=0,
                ctr=None,
                average_view_duration_seconds=None,
                average_percentage_viewed=None,
            )
            imported += 1
            if imported >= max_videos:
                break
        next_page_token = page.get("nextPageToken")
        if not next_page_token:
            break
    return {
        "success": True,
        "channel": {
            "channel_id": channel_id,
            "channel_name": channel_name,
            "subscriber_count": subscriber_count,
            "video_count": video_count,
            "view_count": view_count,
        },
        "imported_videos": imported,
        "pages_read": pages,
        "note": (
            "Public YouTube Data API channel/video statistics imported. "
            "CTR, impressions, average view duration, average percentage "
            "viewed and subscribers gained require YouTube Analytics "
            "authorization."
        ),
    }
def import_real_channel_data(
    channel_id: str = DEFAULT_CHANNEL_ID,
    max_videos: int = 50,
) -> dict:
    return import_channel(
        channel_id=channel_id,
        max_videos=max_videos,
    )
