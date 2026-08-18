import os
import time
import requests
from groq import Groq

# Configuration
TELEGRAM_TOKEN = os.getenv("MINING_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
UPI_ID = "Omnitechai@naviaxis"  # <-- Navi App Verified UPI ID
COMPANY_TREASURY_WALLET = "TEnk27LNfmBKytkXTXeWcY3zWHVgMfw96p"
FREE_LIMIT = 10

groq_client = Groq(api_key=GROQ_API_KEY)

# Database Structure (In-Memory)
USERS = {}  # {chat_id: {"queries": 0, "vip_until": timestamp, "referred_by": id}}

def run_groq(agent_name, role, query):
    try:
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are {agent_name} at OmniTech. {role}. Give direct, sharp, and practical solutions in natural Hinglish/English."},
                {"role": "user", "content": query}
            ],
            max_tokens=400,
            temperature=0.6
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"⚡ Processing Node Busy: {str(e)[:40]}"

def get_user(chat_id):
    if chat_id not in USERS:
        USERS[chat_id] = {"queries": 0, "vip_until": 0, "referred_by": None}
    return USERS[chat_id]

def is_vip(user):
    return time.time() < user["vip_until"]

def send_msg(chat_id, text):
    if not TELEGRAM_TOKEN:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception:
        pass

def send_qr_invoice(chat_id, amount, note):
    # Dynamic UPI QR Image Generator via QuickChart
    upi_payload = f"upi://pay?pa={UPI_ID}&pn=OmniTechAI&am={amount}&cu=INR&tn={note}"
    qr_url = f"https://quickchart.io/qr?text={requests.utils.quote(upi_payload)}&size=300"
    
    caption = (
        f"🇮🇳 **Pay ₹{amount} to Unlock Access**\n\n"
        f"👉 **UPI ID:** `{UPI_ID}`\n"
        f"👉 **Amount:** ₹{amount}\n\n"
        "📸 Upar diya gaya QR Code scan karke pay karein (PhonePe/GPay/Paytm/Navi).\n"
        "Payment ke baad verify karein: `/verify <UTR_Number>`"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": qr_url, "caption": caption, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception:
        send_msg(chat_id, caption)

def send_crypto_invoice(chat_id, amount_usd, months):
    msg = (
        f"🌍 **Global Binance / Crypto Pass ({months} Months VIP)**\n\n"
        f"👉 **Amount:** `{amount_usd} USDT`\n"
        f"👉 **Network:** `TRON (TRC20)`\n"
        f"👉 **Treasury Wallet:**\n`{COMPANY_TREASURY_WALLET}`\n\n"
        "Send USDT to the address above, then confirm via:\n"
        f"`/verify <TXID>`"
    )
    send_msg(chat_id, msg)

def main():
    print("[*] OmniTech Multi-Currency Hybrid Freemium Engine is LIVE with Navi UPI...")
    last_update_id = 0

    while True:
        if TELEGRAM_TOKEN:
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=5"
                resp = requests.get(url, timeout=10).json()
                if resp.get("ok"):
                    for update in resp.get("result", []):
                        last_update_id = update["update_id"]
                        msg = update.get("message", {})
                        chat_id = msg.get("chat", {}).get("id")
                        raw_text = msg.get("text", "").strip()

                        if not raw_text or not chat_id:
                            continue

                        user = get_user(chat_id)
                        bot_user = "OmniTechautoearningBot"

                        # /start Handler
                        if raw_text.startswith("/start"):
                            parts = raw_text.split()
                            if len(parts) > 1 and parts[1].startswith("ref_"):
                                try:
                                    ref_id = int(parts[1].replace("ref_", ""))
                                    if ref_id != chat_id and user["referred_by"] is None:
                                        user["referred_by"] = ref_id
                                except Exception:
                                    pass

                            welcome = (
                                "⚡ **Welcome to OmniTech Super AI Engine!**\n\n"
                                f"🎁 You have **{FREE_LIMIT} FREE AI Queries** available!\n\n"
                                "🔥 **AI Specialist Commands:**\n"
                                "👉 `/signals <coin>` - Live Market Alpha (BTC/SOL)\n"
                                "👉 `/audit <token>` - Smart Contract Security Scan\n"
                                "👉 `/debug <code>` - Instant Code Bug Fixer\n"
                                "👉 `/copy <topic>` - High Converting Ad Copy\n\n"
                                "💎 **Pricing Plans:** `/plans`\n"
                                f"🔗 **Referral Link:** `https://t.me/{bot_user}?start=ref_{chat_id}`\n"
                                "*(Share with friends: Get 1 Month FREE VIP on their purchase!)*"
                            )
                            send_msg(chat_id, welcome)

                        elif raw_text == "/plans":
                            plans_text = (
                                "💎 **OmniTech VIP Pricing Plans:**\n\n"
                                "🇮🇳 **India Plans (UPI QR):**\n"
                                "• 1 Month: ₹9 ➡️ `/buy 9`\n"
                                "• 3 Months: ₹19 ➡️ `/buy 19`\n"
                                "• 6 Months: ₹29 ➡️ `/buy 29`\n"
                                "• 1 Year: ₹39 ➡️ `/buy 39`\n\n"
                                "🌍 **International / Binance (USDT TRC20):**\n"
                                "• 2 Months ($1 USDT) ➡️ `/buycrypto 1`\n"
                                "• 5 Months ($2 USDT) ➡️ `/buycrypto 2`\n"
                                "• 1 Year ($3 USDT) ➡️ `/buycrypto 3`"
                            )
                            send_msg(chat_id, plans_text)

                        elif raw_text.startswith("/buycrypto"):
                            parts = raw_text.split()
                            val = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
                            months_map = {1: 2, 2: 5, 3: 12}
                            months = months_map.get(val, 2)
                            send_crypto_invoice(chat_id, val, months)

                        elif raw_text.startswith("/buy"):
                            parts = raw_text.split()
                            amount = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 9
                            send_qr_invoice(chat_id, amount, f"OmniTech Plan {amount}")

                        elif raw_text.startswith("/verify"):
                            # Plan activation
                            days = 60
                            user["vip_until"] = max(time.time(), user["vip_until"]) + (days * 86400)
                            send_msg(chat_id, f"🎉 **VIP Access Granted!** Plan activated successfully for {days} days.")

                            # Auto Referral Reward (1 Month Free)
                            if user["referred_by"]:
                                ref_user = get_user(user["referred_by"])
                                ref_user["vip_until"] = max(time.time(), ref_user["vip_until"]) + (30 * 86400)
                                send_msg(user["referred_by"], "🎁 **Referral Bonus!** Your friend unlocked a plan. You received **1 Month Free VIP**!")
                                user["referred_by"] = None

                        else:
                            # Quota Engine
                            if not is_vip(user) and user["queries"] >= FREE_LIMIT:
                                send_msg(
                                    chat_id,
                                    "🔒 **10 Free Queries Exhausted!**\n\n"
                                    "Unlock Unlimited VIP Access starting at just ₹9 / $1 USDT.\n"
                                    "👉 Check options: `/plans`"
                                )
                                continue

                            if not is_vip(user):
                                user["queries"] += 1
                                remaining = FREE_LIMIT - user["queries"]
                                status_footer = f"\n\n*(Trial: {user['queries']}/{FREE_LIMIT} used | {remaining} left)*"
                            else:
                                status_footer = "\n\n*(VIP Pass: Unlimited Access)*"

                            send_msg(chat_id, "⏳ *OmniTech AI computing solution...*")
                            res = run_groq("OmniTech AI", "Expert Multi-Domain Consultant", raw_text)
                            send_msg(chat_id, f"{res}{status_footer}")

            except Exception:
                pass

        time.sleep(1)

import subprocess

if __name__ == "__main__":
    subprocess.Popen(["python", "promo.py"])
    main()
    
                        
