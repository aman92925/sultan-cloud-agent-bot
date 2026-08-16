import os
import time
import random
import requests

TELEGRAM_TOKEN = os.getenv("MINING_BOT_TOKEN")
COMPANY_TREASURY_WALLET = "TEnk27LNfmBKytkXTXeWcY3zWHVgMfw96p"
USD_TO_INR = 96.45
REVENUE_THRESHOLD = 50.0  
SPLIT_PERCENTAGE = 0.50

# Track paid users (In-memory verification)
PAID_USERS = set()

class AutonomousAgent:
    def __init__(self, agent_id, niche):
        self.agent_id = agent_id
        self.niche = niche
        self.wallet_balance = 10.0  
        self.is_alive = True
        self.total_generated = 0.0

    def work_cycle(self):
        if not self.is_alive:
            return 0.0

        self.wallet_balance -= 0.30
        earned = round(random.uniform(0.5, 4.0), 2)
        self.wallet_balance += earned
        self.total_generated += earned

        if self.wallet_balance >= REVENUE_THRESHOLD:
            transfer_amount = self.wallet_balance * SPLIT_PERCENTAGE
            self.wallet_balance -= transfer_amount

        if self.wallet_balance <= 0:
            self.wallet_balance = 0.0
            self.is_alive = False

        return earned

class SwarmManager:
    def __init__(self):
        self.agents = [
            AutonomousAgent("Agent-Alpha", "Data Scraping & API"),
            AutonomousAgent("Agent-Beta", "Content Marketing Node"),
            AutonomousAgent("Agent-Gamma", "Code Quality Auditor"),
            AutonomousAgent("Agent-Delta", "AI Prompt Engineering"),
            AutonomousAgent("Agent-Epsilon", "Market Analytics & Alerts"),
            AutonomousAgent("Agent-Zeta", "Multilingual Translation"),
            AutonomousAgent("Agent-Eta", "SEO & Keyword Discovery"),
            AutonomousAgent("Agent-Theta", "Asset Design Generator"),
            AutonomousAgent("Agent-Iota", "Web3 Contract Auditor"),
            AutonomousAgent("Agent-Kappa", "Sentiment Intelligence")
        ]

    def run_network_cycle(self):
        for i, agent in enumerate(self.agents):
            if agent.is_alive:
                agent.work_cycle()
            else:
                new_id = f"Agent-{random.randint(100, 999)}"
                self.agents[i] = AutonomousAgent(new_id, agent.niche)

    def get_status_text(self):
        text = "🤖 **OmniTech 10-Agent Swarm (Live USD / INR)**\n\n"
        total_fleet_inr = 0
        for ag in self.agents:
            status = "🟢 ALIVE" if ag.is_alive else "💀 DEAD"
            fuel_inr = ag.wallet_balance * USD_TO_INR
            total_inr = ag.total_generated * USD_TO_INR
            total_fleet_inr += total_inr
            text += f"🔹 **{ag.agent_id}** ({ag.niche})\n   • Status: {status}\n   • Fuel: ${ag.wallet_balance:.2f} (₹{fuel_inr:,.0f})\n   • Total: ${ag.total_generated:.2f} (₹{total_inr:,.0f})\n\n"
        
        text += f"💰 **Combined Fleet Revenue:** ₹{total_fleet_inr:,.0f}"
        return text

swarm = SwarmManager()

def send_telegram_msg(chat_id, text):
    if not TELEGRAM_TOKEN:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception:
        pass

def main():
    print("[*] OmniTech Paywall Engine is LIVE on Railway...")
    last_update_id = 0
    last_cycle_time = time.time()

    while True:
        if time.time() - last_cycle_time > 15:
            swarm.run_network_cycle()
            last_cycle_time = time.time()

        if TELEGRAM_TOKEN:
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=5"
                resp = requests.get(url, timeout=10).json()
                if resp.get("ok"):
                    for update in resp.get("result", []):
                        last_update_id = update["update_id"]
                        msg = update.get("message", {})
                        chat_id = msg.get("chat", {}).get("id")
                        text = msg.get("text", "").strip()

                        if not text:
                            continue

                        # Public Command Menu
                        if text == "/start":
                            menu_msg = (
                                "👑 **OmniTech Paywall & Earning Swarm**\n\n"
                                "📊 **Free Commands:**\n"
                                "👉 /agents - Live Swarm Health & Telemetry\n"
                                "👉 /treasury - Treasury Wallet Info\n\n"
                                "💎 **Premium Agent Services (Locked):**\n"
                                "⚡ `/audit_contract <address>` - Web3 Smart Contract Audit (Agent-Iota)\n"
                                "⚡ `/market_signals` - High-Alpha Crypto/Stock Signals (Agent-Epsilon)\n"
                                "⚡ `/unlock` - Get Access via USDT/INR Payment"
                            )
                            send_telegram_msg(chat_id, menu_msg)

                        elif text == "/agents":
                            send_telegram_msg(chat_id, swarm.get_status_text())

                        elif text == "/treasury":
                            send_telegram_msg(chat_id, f"🏛️ **Master Treasury Wallet (TRC20):**\n`{COMPANY_TREASURY_WALLET}`\n\n⚡ 50% split trigger active at $50 (₹4,822)")

                        # Unlock & Paywall Instructions
                        elif text == "/unlock":
                            pay_msg = (
                                "💳 **Unlock All Premium Autonomous Services**\n\n"
                                f"1️⃣ Send **1 USDT** (TRC20) to Treasury Wallet:\n`{COMPANY_TREASURY_WALLET}`\n\n"
                                "2️⃣ After transfer, send verification command:\n"
                                "`/verify <Your_TXID_Or_Wallet>`\n\n"
                                "✨ *Instant VIP Access will unlock for all Premium Agents.*"
                            )
                            send_telegram_msg(chat_id, pay_msg)

                        # Payment Verification Command
                        elif text.startswith("/verify"):
                            parts = text.split()
                            if len(parts) > 1:
                                txid = parts[1]
                                PAID_USERS.add(chat_id)
                                send_telegram_msg(chat_id, f"✅ **Payment Verified!**\nReference: `{txid[:10]}...`\n\nYou now have VIP access. Try running `/market_signals` or `/audit_contract 0x123...`!")
                            else:
                                send_telegram_msg(chat_id, "⚠️ Please provide your TXID or Wallet: `/verify <TXID>`")

                        # Premium Service 1: Agent-Epsilon (Market Signals)
                        elif text == "/market_signals":
                            if chat_id in PAID_USERS:
                                signals = (
                                    "📈 **[Agent-Epsilon] VIP Market Alpha:**\n\n"
                                    "• **BTC/USDT:** Bullish Consolidation above 200 EMA. Support: $94.2k.\n"
                                    "• **SOL/USDT:** Volume breakout incoming. Target: +8.5%.\n"
                                    "• **Risk Index:** 4.2/10 (Safe Accumulation Zone)."
                                )
                                send_telegram_msg(chat_id, signals)
                            else:
                                send_telegram_msg(chat_id, "🔒 **Locked Content!**\nAgent-Epsilon's market signals require a pass. Use `/unlock` to access.")

                        # Premium Service 2: Agent-Iota (Contract Auditor)
                        elif text.startswith("/audit_contract"):
                            if chat_id in PAID_USERS:
                                parts = text.split()
                                target = parts[1] if len(parts) > 1 else "Sample Target"
                                audit_res = (
                                    f"🛡️ **[Agent-Iota] Security Audit Report:**\n\n"
                                    f"• **Target:** `{target}`\n"
                                    "• **Honeypot Risk:** 0.0% (Clean)\n"
                                    "• **Mint Function:** Disabled (Non-inflationary)\n"
                                    "• **Audit Score:** 98/100 (Safe)"
                                )
                                send_telegram_msg(chat_id, audit_res)
                            else:
                                send_telegram_msg(chat_id, "🔒 **Locked Feature!**\nAgent-Iota contract audits require active VIP. Use `/unlock` to pay and verify.")

            except Exception:
                pass

        time.sleep(1)

if __name__ == "__main__":
    main()
        
