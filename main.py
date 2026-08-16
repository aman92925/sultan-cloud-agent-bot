import os
import time
import json
import requests
from groq import Groq

# Configuration
TELEGRAM_TOKEN = os.getenv("MINING_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COMPANY_TREASURY_WALLET = "TEnk27LNfmBKytkXTXeWcY3zWHVgMfw96p"
USD_TO_INR = 96.45
MICRO_FEE_USD = 0.10
MICRO_FEE_INR = 10.0

groq_client = Groq(api_key=GROQ_API_KEY)
PAID_USERS = set()

# AI Engine Worker
def run_groq_brain(agent_name, role_prompt, user_query):
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"You are {agent_name}, an autonomous AI operative at OmniTech Corporate. {role_prompt}. Your core target is delivering instant, high-value, crisp business results to maximize client retention and volume sales."
                },
                {"role": "user", "content": user_query}
            ],
            max_tokens=400,
            temperature=0.6
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚡ Node Overload: Re-routing query. Error: {str(e)[:50]}"

# Corporate Multi-Agent Fleet
AGENTS = {
    "audit": {
        "id": "Agent-Iota",
        "dept": "CTO",
        "role": "Web3 & Smart Contract Auditor. Scan addresses and code for exploits, honeypots, and mint functions."
    },
    "signals": {
        "id": "Agent-Epsilon",
        "dept": "CFO",
        "role": "Quantitative Market Analyst. Provide high-accuracy crypto market analysis, support/resistance, and risk assessment."
    },
    "debug": {
        "id": "Agent-Gamma",
        "dept": "CTO",
        "role": "Elite Code Auditor. Detect bugs, optimize performance, and output corrected code."
    },
    "copy": {
        "id": "Agent-Beta",
        "dept": "CMO",
        "role": "Conversion Copywriter. Generate viral hooks, high-converting ad copy, and organic growth threads."
    },
    "prompt": {
        "id": "Agent-Delta",
        "dept": "CTO",
        "role": "Master Prompt Architect. Engineer advanced AI system prompts and business workflows."
    }
}

def send_telegram_msg(chat_id, text, thread_id=None):
    if not TELEGRAM_TOKEN:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if thread_id:
        payload["message_thread_id"] = thread_id
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception:
        pass

def main():
    print("[*] OmniTech AI-Powered Autonomous Fleet is LIVE...")
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
                        thread_id = msg.get("message_thread_id")
                        raw_text = msg.get("text", "").strip()

                        if not raw_text:
                            continue

                        cmd = raw_text.split("@")[0].strip()

                        if cmd == "/start":
                            welcome = (
                                "⚡ **OmniTech High-Volume AI Service Node**\n\n"
                                f"🔥 **Micro-Pricing:** Har AI service sirf **₹{MICRO_FEE_INR:.0f} ($0.10 USDT)**!\n\n"
                                "🤖 **Available AI Agents:**\n"
                                "👉 `/audit <code/token>` - Web3 Contract Audit (Agent-Iota)\n"
                                "👉 `/signals <coin>` - Crypto/Stock Signals (Agent-Epsilon)\n"
                                "👉 `/debug <code>` - Fix & Optimize Code (Agent-Gamma)\n"
                                "👉 `/copy <product>` - High-Converting Copy (Agent-Beta)\n"
                                "👉 `/prompt <task>` - Master Prompt Engine (Agent-Delta)\n\n"
                                "💳 **Payment & Access:**\n"
                                "👉 `/unlock` - Get Unlimited VIP Access Pass"
                            )
                            send_telegram_msg(chat_id, welcome, thread_id)

                        elif cmd == "/unlock":
                            pay_msg = (
                                "💳 **OmniTech Micro-Access Pass**\n\n"
                                f"Send **1 USDT** (Unlimited Pass) or **₹10 UPI** to Treasury:\n"
                                f"TRC20 Wallet: `{COMPANY_TREASURY_WALLET}`\n\n"
                                "Send verification: `/verify <TXID_or_UTR>`"
                            )
                            send_telegram_msg(chat_id, pay_msg, thread_id)

                        elif cmd.startswith("/verify"):
                            PAID_USERS.add(chat_id)
                            send_telegram_msg(chat_id, "✅ **Access Granted!** Sabhi Groq AI Agents aapke liye live ho chuke hain. Koi bhi command run karein!", thread_id)

                        # AI Service: Web3 Contract Audit
                        elif cmd.startswith("/audit"):
                            if chat_id not in PAID_USERS:
                                send_telegram_msg(chat_id, "🔒 Micro-pass required. Run `/unlock` to access.", thread_id)
                                continue
                            query = cmd.replace("/audit", "").strip() or "Standard ERC20 Token Contract"
                            send_telegram_msg(chat_id, "⏳ *Agent-Iota analyzing contract with Groq Llama-3...*", thread_id)
                            res = run_groq_brain(AGENTS["audit"]["id"], AGENTS["audit"]["role"], query)
                            send_telegram_msg(chat_id, f"🛡️ **[Agent-Iota Security Report]**\n\n{res}", thread_id)

                        # AI Service: Market Signals
                        elif cmd.startswith("/signals"):
                            if chat_id not in PAID_USERS:
                                send_telegram_msg(chat_id, "🔒 Micro-pass required. Run `/unlock` to access.", thread_id)
                                continue
                            query = cmd.replace("/signals", "").strip() or "BTC and Solana market outlook"
                            send_telegram_msg(chat_id, "⏳ *Agent-Epsilon scanning order books...*", thread_id)
                            res = run_groq_brain(AGENTS["signals"]["id"], AGENTS["signals"]["role"], query)
                            send_telegram_msg(chat_id, f"📈 **[Agent-Epsilon Alpha Signal]**\n\n{res}", thread_id)

                        # AI Service: Code Debugger
                        elif cmd.startswith("/debug"):
                            if chat_id not in PAID_USERS:
                                send_telegram_msg(chat_id, "🔒 Micro-pass required. Run `/unlock` to access.", thread_id)
                                continue
                            query = cmd.replace("/debug", "").strip() or "def hello(): pirnt('error')"
                            send_telegram_msg(chat_id, "⏳ *Agent-Gamma auditing syntax & logic...*", thread_id)
                            res = run_groq_brain(AGENTS["debug"]["id"], AGENTS["debug"]["role"], query)
                            send_telegram_msg(chat_id, f"🛠️ **[Agent-Gamma Debug Output]**\n\n{res}", thread_id)

                        # AI Service: Copywriting
                        elif cmd.startswith("/copy"):
                            if chat_id not in PAID_USERS:
                                send_telegram_msg(chat_id, "🔒 Micro-pass required. Run `/unlock` to access.", thread_id)
                                continue
                            query = cmd.replace("/copy", "").strip() or "AI Automation SaaS tool"
                            send_telegram_msg(chat_id, "⏳ *Agent-Beta generating high-conversion copy...*", thread_id)
                            res = run_groq_brain(AGENTS["copy"]["id"], AGENTS["copy"]["role"], query)
                            send_telegram_msg(chat_id, f"📢 **[Agent-Beta Copy Engine]**\n\n{res}", thread_id)

            except Exception:
                pass

        time.sleep(1)

if __name__ == "__main__":
    main()
                            
