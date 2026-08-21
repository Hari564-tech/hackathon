import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """
    Abstract base class for all hackathon platform scrapers.
    Ensures normalized output schema across Devfolio, Unstop, Devpost, etc.
    """
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    def __init__(self, platform_name: str):
        self.platform_name = platform_name

    @abstractmethod
    def fetch_hackathons(self) -> List[Dict[str, Any]]:
        """
        Fetch and parse hackathons from the platform.
        Returns a list of standardized hackathon dictionaries.
        """
        pass

    def normalize_mode(self, raw_mode: Optional[str], raw_text: str = "") -> str:
        """
        Determines if the hackathon is Online, Offline (In-Person), or Hybrid.
        """
        if raw_mode:
            m = raw_mode.strip().lower()
            if "online" in m or "virtual" in m or "remote" in m:
                return "Online"
            if "hybrid" in m or "blended" in m:
                return "Hybrid"
            if "offline" in m or "in_person" in m or "in-person" in m or "physical" in m or "on-site" in m:
                return "Offline"

        # Heuristic fallback on page text
        lower_text = raw_text.lower()
        if "online" in lower_text or "virtual" in lower_text or "remote hackathon" in lower_text:
            return "Online"
        elif "hybrid" in lower_text:
            return "Hybrid"
        return "Offline"
