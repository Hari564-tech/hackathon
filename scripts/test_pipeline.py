#!/usr/bin/env python3
"""
Integration & Validation Test Suite for HackRadar India.
Checks data consistency, required schema fields, and pipeline execution.
"""

import json
import os
import sys

def run_tests():
    data_path = os.path.join(os.path.dirname(__file__), "../frontend/data/hackathons.json")
    print(f"[TEST] Checking dataset at: {data_path}")

    assert os.path.exists(data_path), "hackathons.json does not exist!"

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "hackathons" in data, "Root key 'hackathons' missing!"
    items = data["hackathons"]
    print(f"[TEST] Total Hackathons Loaded: {len(items)}")
    assert len(items) > 0, "Hackathon list is empty!"

    required_fields = ["title", "source_url", "mode", "venue_address", "banner_url", "deadline", "prize_pool"]

    seen_urls = set()
    for idx, item in enumerate(items):
        for field in required_fields:
            assert field in item and item[field], f"Missing or empty '{field}' in item #{idx}: {item.get('title')}"
        
        # Check Mode
        assert item["mode"] in ["Online", "Offline", "Hybrid"], f"Invalid mode '{item['mode']}' in item #{idx}"
        
        # Check Banner URL
        assert item["banner_url"].startswith("http"), f"Invalid banner URL in item #{idx}"

        # Deduplication check
        assert item["source_url"] not in seen_urls, f"Duplicate source URL found: {item['source_url']}"
        seen_urls.add(item["source_url"])

    print("==================================================")
    print(" ALL PIPELINE & SCHEMA TESTS PASSED SUCCESSFULLY! ")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
