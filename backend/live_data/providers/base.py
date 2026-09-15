from live_data.models import LiveData
from abc import ABC, abstractmethod
class LiveDataProvider(ABC):
    name = "base"
    @abstractmethod
    def fetch(self, topic: str, **kwargs) -> LiveData:
        raise NotImplementedError
