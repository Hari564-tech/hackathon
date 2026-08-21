# ⚡ HackRadar India — Automated Hackathon Tracker & Web Platform

> A full-stack, automated platform that aggregates, normalizes, and showcases upcoming hackathons across India in real-time. Automatically parses event posters, online/offline status, venue addresses, prize pools, and registration deadlines.

---

## 🏗️ Architecture Overview

```
[Sources: Devfolio, Unstop, Devpost, SIH]
                     │
                     ▼
 [Automated Cron Runner: GitHub Actions (Every 6 hrs)]
                     │
       ┌─────────────┴─────────────┐
       ▼                           ▼
[PostgreSQL / Supabase]   [JSON Snapshot Store]
       │                           │
       └─────────────┬─────────────┘
                     ▼
     [Frontend: Glassmorphic Web App]
   (Live Filters, Mode Badges, Posters, 
    Addresses, Countdowns, 1-Click Calendar)
                     │
                     ▼
     [Telegram & Discord Alerts]
```

---

## ✨ Features

1. **Automated Synchronization (GitHub Actions Cron)**:
   - Scrapes multiple developer platforms on a scheduled cadence (every 6 hours).
   - Deduplicates records and updates both cloud database (Supabase) and static data snapshots.

2. **Accurate Mode & Venue Address Detection**:
   - Explicitly badges events as **🌐 Online (Virtual)**, **📍 In-Person (Offline)**, or **🔀 Hybrid**.
   - Extracts complete campus and city addresses (e.g. *Neerukonda Campus, Mangalagiri, Amaravati, Andhra Pradesh*, *Koramangala, Bengaluru*).

3. **High-Resolution Poster & Banner Imagery**:
   - Captures Open Graph banners and event artwork with responsive image fallbacks and lazy-loading.

4. **Real-Time Registration Countdown**:
   - Dynamic countdown clock calculating days and hours left until registration closes. Highlights urgent deadlines in rose/amber.

5. **Multi-Faceted Search & Filters**:
   - Instant search across titles, organizers, and tech tags.
   - Filter by City (Bengaluru, Hyderabad, Amaravati, Delhi NCR, etc.), Mode (Online vs Offline), and Themes (AI/ML, Web3, FinTech, GovTech/SIH).

6. **1-Click Google Calendar Integration**:
   - Automatically populates the event title, deadline, location, and application URL into Google Calendar.

7. **Community Submission Portal**:
   - Allows college fest and community organizers to submit upcoming hackathons directly with instant local preview.

8. **Telegram & Discord Broadcast Webhooks**:
   - Automatically dispatches rich notification embeds whenever a new hackathon is detected.

---

## 🚀 Quick Start Guide

### 1. Clone & Install Dependencies
```bash
cd automation
pip install -r requirements.txt
```

### 2. Run the Ingestion Pipeline Locally
```bash
python run_sync.py
```
*This populates `frontend/data/hackathons.json` with the latest scraped and enriched hackathon entries.*

### 3. Launch the Frontend
You can launch the web application with any local HTTP server:
```bash
cd ../frontend
python3 -m http.server 8080
```
Open `http://localhost:8080` in your web browser.

---

## ⚙️ Environment Variables (Optional for Cloud Setup)

| Variable | Description |
| :--- | :--- |
| `SUPABASE_URL` | Supabase project URL for PostgreSQL persistence |
| `SUPABASE_KEY` | Supabase service key / anon key |
| `TELEGRAM_BOT_TOKEN` | Bot token for Telegram alert broadcasts |
| `TELEGRAM_CHAT_ID` | Telegram channel or group chat ID |
| `DISCORD_WEBHOOK_URL`| Discord webhook URL for new hackathon alerts |

---

## 📦 Production Deployment

1. **Frontend Hosting**: Deploy directly to **Vercel** or **Cloudflare Pages** by connecting your GitHub repository.
2. **Scheduled Sync**: The included `.github/workflows/sync_hackathons.yml` automatically runs every 6 hours to fetch fresh competitions and commit the updated data.
