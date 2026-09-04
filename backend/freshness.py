from datetime import datetime, timedelta, timezone
from typing import Optional
class FreshnessEngine:
    # Default TTLs in minutes
    TTL_POLICY = {
        'finance': 15,        # 15 minutes
        'weather': 60,        # 1 hour
        'sports': 60,         # 1 hour
        'news': 1440,         # 24 hours (1 day)
        'general_live': 10080 # 7 days
    }
    @classmethod
    def calculate_expiry(cls, topic: str, knowledge_type: str) -> Optional[str]:
        '''
        Calculates ISO format expiry timestamp based on knowledge type and topic.
        Returns None for permanent knowledge.
        '''
        if knowledge_type == 'permanent':
            return None
        topic_clean = (topic or '').lower().strip()
        minutes = cls.TTL_POLICY.get('general_live', 10080)
        if any(k in topic_clean for k in ['stock', 'price', 'crypto', 'finance', 'market']):
            minutes = cls.TTL_POLICY['finance']
        elif any(k in topic_clean for k in ['weather', 'temperature', 'rain', 'score', 'match', 'sports']):
            minutes = cls.TTL_POLICY['weather']
        elif any(k in topic_clean for k in ['news', 'today', 'event', 'current', 'latest']):
            minutes = cls.TTL_POLICY['news']
        exp_time = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        return exp_time.isoformat()
