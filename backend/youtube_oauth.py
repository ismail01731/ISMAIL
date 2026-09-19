from __future__ import annotations
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
ENV_PATH = Path(r"D:\ISMAIL\config\.env")
load_dotenv(ENV_PATH)
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
YOUTUBE_ANALYTICS_SCOPE = (
    "https://www.googleapis.com/auth/yt-analytics.readonly"
)
YOUTUBE_READONLY_SCOPE = (
    "https://www.googleapis.com/auth/youtube.readonly"
)
class YouTubeOAuthManager:
    def __init__(self) -> None:
        load_dotenv(ENV_PATH)
        self.client_id = (
            os.getenv("GOOGLE_CLIENT_ID", "").strip()
        )
        self.client_secret = (
            os.getenv("GOOGLE_CLIENT_SECRET", "").strip()
        )
        self.channel_id = (
            os.getenv(
                "YOUTUBE_CHANNEL_ID",
                "UCP75FPRq4DaMoe88G9R3heg",
            ).strip()
        )
        self.scopes = [
            YOUTUBE_ANALYTICS_SCOPE,
            YOUTUBE_READONLY_SCOPE,
        ]
        self.access_token = None
        self.refresh_token = (
            os.getenv(
                "YOUTUBE_REFRESH_TOKEN",
                "",
            ).strip()
        )
        self.token_type = None
    def configuration_status(self) -> dict[str, Any]:
        return {
            "client_id_configured": bool(
                self.client_id
            ),
            "client_secret_configured": bool(
                self.client_secret
            ),
            "oauth_ready": bool(
                self.client_id
                and self.client_secret
            ),
        }
    def create_authorization_url(
        self,
        redirect_uri: str,
        state: str,
    ) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
        }
        return (
            GOOGLE_AUTH_URL
            + "?"
            + urllib.parse.urlencode(params)
        )
    def _save_refresh_token(
        self,
        refresh_token: str,
    ) -> None:
        refresh_token = (
            str(refresh_token or "").strip()
        )
        if not refresh_token:
            return
        if ENV_PATH.exists():
            lines = ENV_PATH.read_text(
                encoding="utf-8"
            ).splitlines()
        else:
            lines = []
        key = "YOUTUBE_REFRESH_TOKEN="
        replacement = key + refresh_token
        found = False
        for index, line in enumerate(lines):
            if line.strip().startswith(key):
                lines[index] = replacement
                found = True
                break
        if not found:
            lines.append(replacement)
        ENV_PATH.write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )
        os.environ["YOUTUBE_REFRESH_TOKEN"] = (
            refresh_token
        )
    def exchange_code(
        self,
        code: str,
        redirect_uri: str,
    ) -> dict[str, Any]:
        if not self.client_id or not self.client_secret:
            return {
                "success": False,
                "error": (
                    "Google OAuth configuration "
                    "is incomplete."
                ),
            }
        code = str(code or "").strip()
        if not code:
            return {
                "success": False,
                "error": (
                    "OAuth authorization code "
                    "is missing."
                ),
            }
        payload = urllib.parse.urlencode({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }).encode("utf-8")
        request = urllib.request.Request(
            GOOGLE_TOKEN_URL,
            data=payload,
            method="POST",
            headers={
                "Content-Type": (
                    "application/x-www-form-urlencoded"
                ),
                "Accept": "application/json",
                "User-Agent": (
                    "ISMAIL-AI-YouTube-OAuth/1.0"
                ),
            },
        )
        try:
            with urllib.request.urlopen(
                request,
                timeout=60,
            ) as response:
                raw = response.read().decode(
                    "utf-8",
                    errors="replace",
                )
            data = json.loads(raw)
        except Exception as exc:
            return {
                "success": False,
                "error": (
                    "OAuth token exchange failed: "
                    f"{type(exc).__name__}"
                ),
            }
        access_token = str(
            data.get("access_token", "")
        ).strip()
        if not access_token:
            return {
                "success": False,
                "error": data.get(
                    "error_description",
                    data.get(
                        "error",
                        "Google did not return "
                        "an access token.",
                    ),
                ),
            }
        refresh_token = str(
            data.get("refresh_token", "")
        ).strip()
        self.access_token = access_token
        if refresh_token:
            self.refresh_token = refresh_token
            self._save_refresh_token(
                refresh_token
            )
        self.token_type = (
            str(
                data.get(
                    "token_type",
                    "",
                )
            ).strip()
            or None
        )
        return {
            "success": True,
            "authenticated": True,
            "channel_id": self.channel_id,
            "refresh_token_received": bool(
                refresh_token
            ),
            "scope": data.get(
                "scope",
                "",
            ),
        }
    def refresh_access_token(self) -> dict[str, Any]:
        refresh_token = (
            str(
                self.refresh_token
                or os.getenv(
                    "YOUTUBE_REFRESH_TOKEN",
                    "",
                )
            ).strip()
        )
        if not refresh_token:
            return {
                "success": False,
                "error": (
                    "Refresh token is not available."
                ),
            }
        if not self.client_id or not self.client_secret:
            return {
                "success": False,
                "error": (
                    "Google OAuth configuration "
                    "is incomplete."
                ),
            }
        payload = urllib.parse.urlencode({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }).encode("utf-8")
        request = urllib.request.Request(
            GOOGLE_TOKEN_URL,
            data=payload,
            method="POST",
            headers={
                "Content-Type": (
                    "application/x-www-form-urlencoded"
                ),
                "Accept": "application/json",
                "User-Agent": (
                    "ISMAIL-AI-YouTube-OAuth/1.0"
                ),
            },
        )
        try:
            with urllib.request.urlopen(
                request,
                timeout=60,
            ) as response:
                raw = response.read().decode(
                    "utf-8",
                    errors="replace",
                )
            data = json.loads(raw)
        except Exception as exc:
            return {
                "success": False,
                "error": (
                    "OAuth refresh failed: "
                    f"{type(exc).__name__}"
                ),
            }
        access_token = str(
            data.get("access_token", "")
        ).strip()
        if not access_token:
            return {
                "success": False,
                "error": data.get(
                    "error_description",
                    data.get(
                        "error",
                        "Google did not return "
                        "a refreshed access token.",
                    ),
                ),
            }
        self.access_token = access_token
        self.token_type = (
            str(
                data.get(
                    "token_type",
                    "",
                )
            ).strip()
            or self.token_type
            or None
        )
        return {
            "success": True,
            "authenticated": True,
            "channel_id": self.channel_id,
            "refresh_token_used": True,
            "access_token_refreshed": True,
        }
    def authentication_status(self) -> dict[str, Any]:
        return {
            "authenticated": bool(
                self.access_token
                or self.refresh_token
                or os.getenv(
                    "YOUTUBE_REFRESH_TOKEN",
                    "",
                ).strip()
            ),
            "channel_id": self.channel_id,
            "access_token_available": bool(
                self.access_token
            ),
            "refresh_token_available": bool(
                self.refresh_token
                or os.getenv(
                    "YOUTUBE_REFRESH_TOKEN",
                    "",
                ).strip()
            ),
        }
youtube_oauth = YouTubeOAuthManager()
