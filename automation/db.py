import json
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Handles persisting and upserting hackathon events.
    Supports both Supabase (Cloud PostgreSQL) and Static JSON fallback for instant web deployment.
    """
    def __init__(self, json_output_path: str = "../frontend/data/hackathons.json"):
        self.json_output_path = json_output_path
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.supabase_client = None

        if self.supabase_url and self.supabase_key:
            try:
                from supabase import create_client
                self.supabase_client = create_client(self.supabase_url, self.supabase_key)
                logger.info("Connected to Supabase PostgreSQL.")
            except Exception as e:
                logger.warning(f"Could not connect to Supabase: {e}. Using JSON datastore.")

    def upsert_hackathons(self, hackathons: List[Dict[str, Any]]) -> int:
        """
        Upserts hackathons based on unique source_url.
        Returns count of stored records.
        """
        # 1. Store in Supabase if configured
        if self.supabase_client:
            try:
                for h in hackathons:
                    self.supabase_client.table("hackathons").upsert(
                        h, on_conflict="source_url"
                    ).execute()
                logger.info(f"Successfully upserted {len(hackathons)} events into Supabase.")
            except Exception as e:
                logger.error(f"Error upserting to Supabase: {e}")

        # 2. Store in local JSON snapshot for static frontend / API
        os.makedirs(os.path.dirname(os.path.abspath(self.json_output_path)), exist_ok=True)
        
        # Merge with existing data if present
        existing_map = {}
        if os.path.exists(self.json_output_path):
            try:
                with open(self.json_output_path, "r", encoding="utf-8") as f:
                    old_data = json.load(f)
                    for item in old_data.get("hackathons", []):
                        if item.get("source_url"):
                            existing_map[item["source_url"]] = item
            except Exception:
                pass

        # Update / Insert new items
        for h in hackathons:
            existing_map[h["source_url"]] = h

        merged_list = list(existing_map.values())
        
        # Sort by deadline or start date
        merged_list.sort(key=lambda x: x.get("deadline") or "9999", reverse=False)

        import datetime
        snapshot = {
            "last_synced_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "total_count": len(merged_list),
            "hackathons": merged_list
        }

        with open(self.json_output_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(merged_list)} hackathons to {self.json_output_path}.")
        return len(merged_list)
