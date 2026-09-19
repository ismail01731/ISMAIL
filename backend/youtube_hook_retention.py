from typing import Optional
from backend.youtube_growth import analyze_hook_retention
class YouTubeHookRetentionIntelligence:
    """
    Task 7 intelligence layer for hook and retention analysis.
    """
    def analyze(
        self,
        channel_id: Optional[str] = None,
        limit: int = 20,
    ):
        return analyze_hook_retention(
            channel_id=channel_id,
            limit=limit,
        )
hook_retention_intelligence = YouTubeHookRetentionIntelligence()
