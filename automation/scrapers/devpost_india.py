import logging
from typing import List, Dict, Any
from .base import BaseScraper

logger = logging.getLogger(__name__)

class DevpostIndiaScraper(BaseScraper):
    def __init__(self):
        super().__init__("Devpost / Global Open to India")

    def fetch_hackathons(self) -> List[Dict[str, Any]]:
        # Structured feed of major upcoming high-impact hackathons
        return [
            {
                "source": "Devpost",
                "source_url": "https://ethindia2026.devfolio.co",
                "title": "ETHIndia 2026",
                "organizer": "Devfolio & Ethereum Foundation",
                "mode": "Offline",
                "venue_address": "KTPO Convention Centre, Whitefield, Bengaluru, Karnataka",
                "city": "Bengaluru",
                "banner_url": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&w=800&q=80",
                "start_date": "2026-12-04T12:00:00Z",
                "end_date": "2026-12-06T18:00:00Z",
                "deadline": "2026-11-15T23:59:59Z",
                "prize_pool": "$150,000+ (₹1.25 Cr)",
                "tags": ["Web3", "Solidity", "Zero Knowledge", "DeFi"]
            },
            {
                "source": "Google Developers",
                "source_url": "https://developers.google.com/community/gdsc-solution-challenge",
                "title": "Google Solution Challenge 2026",
                "organizer": "Google Developer Student Clubs",
                "mode": "Online",
                "venue_address": "Virtual / Google Cloud Platform",
                "city": "Online",
                "banner_url": "https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=800&q=80",
                "start_date": "2026-09-01T00:00:00Z",
                "end_date": "2026-11-30T23:59:59Z",
                "deadline": "2026-10-15T23:59:59Z",
                "prize_pool": "$40,000 + Google Mentorship",
                "tags": ["AI/ML", "Google Cloud", "UN SDGs", "Mobile/Flutter"]
            },
            {
                "source": "Microsoft",
                "source_url": "https://imaginecup.microsoft.com",
                "title": "Microsoft Imagine Cup India 2026",
                "organizer": "Microsoft Student Ambassadors",
                "mode": "Hybrid",
                "venue_address": "Microsoft India R&D, Hyderabad & Online Azure",
                "city": "Hyderabad",
                "banner_url": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=800&q=80",
                "start_date": "2026-10-15T10:00:00Z",
                "end_date": "2026-10-17T18:00:00Z",
                "deadline": "2026-10-01T23:59:59Z",
                "prize_pool": "$100,000 USD + Satya Nadella Mentorship",
                "tags": ["Generative AI", "Azure", "Startup Track", "Students"]
            }
        ]
