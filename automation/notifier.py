import os
import requests
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class NotificationDispatcher:
    """
    Dispatches alerts to Telegram / Discord when a new hackathon is detected.
    """
    def __init__(self):
        self.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def notify_new_hackathon(self, event: Dict[str, Any]):
        """Broadcasts hackathon details to configured channels."""
        self._send_telegram(event)
        self._send_discord(event)

    def _send_telegram(self, event: Dict[str, Any]):
        if not self.telegram_bot_token or not self.telegram_chat_id:
            return
        
        mode_icon = "🌐" if event["mode"] == "Online" else "📍"
        message = (
            f"🚀 *New Hackathon Alert: {event['title']}*\n\n"
            f"🏢 *Organizer:* {event.get('organizer', 'N/A')}\n"
            f"{mode_icon} *Mode:* {event['mode']} ({event.get('venue_address', 'India')})\n"
            f"💰 *Prize Pool:* {event.get('prize_pool', 'Exciting Rewards')}\n"
            f"⏰ *Deadline:* {event.get('deadline', 'Check Website')}\n\n"
            f"👉 [Apply Here]({event['source_url']})"
        )
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        try:
            requests.post(url, json={"chat_id": self.telegram_chat_id, "text": message, "parse_mode": "Markdown"}, timeout=5)
            logger.info(f"Telegram notification sent for {event['title']}")
        except Exception as e:
            logger.error(f"Telegram error: {e}")

    def _send_discord(self, event: Dict[str, Any]):
        if not self.discord_webhook_url:
            return

        embed = {
            "title": f"🚀 {event['title']}",
            "url": event["source_url"],
            "color": 3447003 if event["mode"] == "Online" else 15105570,
            "fields": [
                {"name": "Organizer", "value": event.get("organizer", "N/A"), "inline": True},
                {"name": "Mode & Location", "value": f"{event['mode']} - {event.get('venue_address', '')}", "inline": True},
                {"name": "Prize Pool", "value": str(event.get("prize_pool", "TBA")), "inline": True},
                {"name": "Deadline", "value": str(event.get("deadline", "Open")), "inline": True},
            ],
            "image": {"url": event["banner_url"]}
        }
        try:
            requests.post(self.discord_webhook_url, json={"embeds": [embed]}, timeout=5)
            logger.info(f"Discord notification sent for {event['title']}")
        except Exception as e:
            logger.error(f"Discord error: {e}")
