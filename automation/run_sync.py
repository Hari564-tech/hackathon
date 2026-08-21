#!/usr/bin/env python3
"""
HackRadar India - Master Automated Synchronization Pipeline
Runs scrapers across all Indian & global hackathon platforms, normalizes metadata,
extracts banners, addresses, and mode, and persists to database and frontend storage.
"""

import sys
import os
import logging
from typing import List, Dict, Any

# Ensure module path resolution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrapers.devfolio import DevfolioScraper
from scrapers.unstop import UnstopScraper
from scrapers.devpost_india import DevpostIndiaScraper
from enricher import HackathonEnricher
from db import DatabaseManager
from notifier import NotificationDispatcher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("HackRadarSync")

def run_pipeline():
    logger.info("==================================================")
    logger.info("Starting Automated Hackathon Ingestion for India")
    logger.info("==================================================")

    scrapers = [
        DevfolioScraper(),
        UnstopScraper(),
        DevpostIndiaScraper()
    ]

    all_raw_events: List[Dict[str, Any]] = []

    for scraper in scrapers:
        try:
            logger.info(f"Running scraper: {scraper.platform_name}...")
            events = scraper.fetch_hackathons()
            logger.info(f"Scraped {len(events)} items from {scraper.platform_name}")
            all_raw_events.extend(events)
        except Exception as e:
            logger.error(f"Scraper {scraper.platform_name} encountered an error: {e}")

    logger.info(f"Total raw events aggregated: {len(all_raw_events)}")

    # Clean & enrich
    enriched_events = []
    for idx, event in enumerate(all_raw_events):
        enriched = HackathonEnricher.clean_event(event, index=idx)
        enriched_events.append(enriched)

    # Database and JSON Snapshot Sync
    # Target relative path to frontend data directory
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../frontend/data/hackathons.json")
    db = DatabaseManager(json_output_path=json_path)
    total_stored = db.upsert_hackathons(enriched_events)

    # Notifications (optional)
    notifier = NotificationDispatcher()
    # Dispatch alerts for top upcoming events if tokens configured
    for event in enriched_events[:2]:
        notifier.notify_new_hackathon(event)

    logger.info("==================================================")
    logger.info(f"Pipeline Completed Successfully! {total_stored} hackathons active.")
    logger.info(f"Frontend data updated at: {json_path}")
    logger.info("==================================================")

if __name__ == "__main__":
    run_pipeline()
