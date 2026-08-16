import os
import time
import requests

BOT_TOKEN = os.getenv("MINING_BOT_TOKEN")
MAIN_BOT_LINK = "https://t.me/OmniTechautoearningBot"

# Promotion target groups (Public discussion group IDs ya usernames)
TARGET_GROUPS = [
    {"chat_id": "@crypto_discussion_hub", "niche": "crypto"},
    {"chat_id": "@python_coders_club", "niche": "dev"},
    {"chat_id": "@freelance_copywriters", "niche": "copy"}
]

PROMO_MESSAGES = {
    "crypto": f"🚀 Memecoin scanner ya BTC targets chahiye? Test 3 free instant AI audit/signal runs: {MAIN_BOT_LINK}",
    "dev": f"🛠️ Code me syntax bug hai? Instant fix pao AI engine se (3 free runs): {MAIN_BOT_LINK}",
    "copy": f"✍️ Ad copy aur sales hooks generate karo 5 seconds me: {MAIN_BOT_LINK}"
}

def dispatch():
    for target in TARGET_GROUPS:
        msg = PROMO_MESSAGES.get(target["niche"])
        if not BOT_TOKEN:
            return
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": target["chat_id"], "text": msg}
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception:
            pass
        time.sleep(900)  # Safe delay: 15 minutes between posts

if __name__ == "__main__":
    while True:
        dispatch()
      
