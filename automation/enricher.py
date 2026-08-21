import re
from typing import Dict, Any

class HackathonEnricher:
    """
    Enriches and cleans raw hackathon metadata.
    Ensures high visual quality (images, clean addresses, proper badges).
    """
    DEFAULT_FALLBACK_IMAGES = [
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=1200&q=80"
    ]

    @classmethod
    def clean_event(cls, item: Dict[str, Any], index: int = 0) -> Dict[str, Any]:
        # Validate banner image
        banner = item.get("banner_url")
        if not banner or not banner.startswith("http"):
            banner = cls.DEFAULT_FALLBACK_IMAGES[index % len(cls.DEFAULT_FALLBACK_IMAGES)]
        item["banner_url"] = banner

        # Ensure valid mode
        mode = item.get("mode") or "Offline"
        if mode not in ["Online", "Offline", "Hybrid"]:
            mode = "Offline"
        item["mode"] = mode

        # Clean address
        venue = item.get("venue_address") or ""
        if mode == "Online" and not venue:
            item["venue_address"] = "Virtual / Discord & YouTube Live"
            item["city"] = "Online"
        elif not venue:
            item["venue_address"] = f"{item.get('organizer', 'Campus Venue')}, India"

        # Ensure tags
        tags = item.get("tags") or []
        if not isinstance(tags, list) or len(tags) == 0:
            tags = ["Coding", "Innovation", "Student Track"]
        item["tags"] = tags[:5]

        # Prize formatting
        prize = item.get("prize_pool") or "₹1,00,000+"
        item["prize_pool"] = prize

        return item
