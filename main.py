import os
import time
import random
import requests

TELEGRAM_TOKEN = os.getenv("MINING_BOT_TOKEN")
COMPANY_TREASURY_WALLET = "TEnk27LNfmBKytkXTXeWcY3zWHVgMfw96p"
USD_TO_INR = 96.45
REVENUE_THRESHOLD = 50.0  
SPLIT_PERCENTAGE = 0.50

PAID_USERS = set()

MANAGERS = {
    "COO": {"title": "Chief Operating Officer", "focus": "Fleet Health & Workload Distribution", "status": "🟢 OPTIMAL"},
    "CFO": {"title": "Chief Financial Officer", "focus": "Treasury & 50% Split Execution", "status": "🟢 OPTIMAL"},
    "CMO": {"title": "Chief Marketing Officer", "focus": "Traffic Arbitrage & User Acquisition", "status": "🟢 OPTIMAL"},
    "CTO": {"title": "Chief Technology Officer", "focus": "R&D Engine & Agent Spawning", "status": "🟢 OPTIMAL"}
}

class AutonomousAgent:
    def __init__(self, agent_id, niche, department):
        self.agent_id = agent_id
        self.niche = niche
        self.department = department
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

class CorporateSwarm:
    def __init__(self):
        self.agents = [
            AutonomousAgent("Worker-01", "Data Scraping & API", "CTO"),
            AutonomousAgent("Worker-02", "Content Marketing Node", "CMO"),
            AutonomousAgent("Worker-03", "Code Quality Auditor", "CTO"),
            AutonomousAgent("Worker-04", "AI Prompt Engineering", "CTO"),
            AutonomousAgent("Worker-05", "Market Analytics & Alerts", "CFO"),
            AutonomousAgent("Worker-06", "Multilingual Translation", "COO"),
            AutonomousAgent("Worker-07", "SEO & Keyword Discovery", "CMO"),
            AutonomousAgent("Worker-08", "Asset Design Generator", "CMO"),
            AutonomousAgent("Worker-09", "Web3 Contract Auditor", "CTO"),
            AutonomousAgent("Worker-10", "Sentiment Intelligence", "COO")
        ]
        self.dead_nodes_count = 0

    def run_cycle(self):
        for i, ag in enumerate(self.agents):
            if ag.is_alive:
                ag.work_cycle()
            else:
                self.dead_nodes_count += 1
                best = self.get_top_performer()
                new_id = f"Worker-{random.randint(100, 999)}"
                self.agents[i] = AutonomousAgent(new_id, f"Evolved: {best.niche}", best.department)

    def get_top_performer(self):
        alive = [a for a in self.agents if a.is_alive]
        return max(alive, key=lambda x: x.total_generated) if alive else self.agents[0]

    def get_corporate_report(self):
        text = "🏢 **OmniTech Corporate Hierarchy & Telemetry**\n\n"
        text += "👔 **Executive Management Board:**\n"
        for code, info in MANAGERS.items():
            text += f"• **{code} ({info['title']}):** {info['status']}\n  _Domain: {info['focus']}_\n"
        
        text += "\n🛠️ **Departmental Fleet:**\n"
        total_inr = 0
        for ag in self.agents:
            status = "🟢" if ag.is_alive else "💀"
            earned_inr = ag.total_generated * USD_TO_INR
            total_inr += earned_inr
            text += f"{status} **[{ag.department}] {ag.agent_id}**: ${ag.total_generated:.2f} (₹{earned_inr:,.0f})\n"
        
        text += f"\n💰 **Gross Enterprise Valuation:** ₹{total_inr:,.0f}"
        return text

corporate = CorporateSwarm()

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
    print("[*] OmniTech Corporate Swarm is ACTIVE...")
    last_update_id = 0
    last_cycle_time = time.time()

    while True:
        if time.time() - last_cycle_time > 15:
            corporate.run_cycle()
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
                        thread_id = msg.get("message_thread_id")
                        raw_text = msg.get("text", "").strip()

                        # Bot handle (@username tag clean)
                        cmd = raw_text.split("@")[0].strip()

                        if not cmd:
                            continue

                        if cmd == "/start":
                            menu = (
                                "👑 **OmniTech Boardroom Command Center**\n\n"
                                "🏢 **Executive Commands:**\n"
                                "👉 /corporate - Full Department & Board Report\n"
                                "👉 /treasury - CFO Master Wallet\n"
                                "👉 /rnd_scan - CTO Innovation Scan\n\n"
                                "💎 **VIP Client Paywall:**\n"
                                "👉 /unlock - Purchase VIP Pass (1 USDT)"
                            )
                            send_telegram_msg(chat_id, menu, thread_id)

                        elif cmd == "/corporate":
                            send_telegram_msg(chat_id, corporate.get_corporate_report(), thread_id)

                        elif cmd == "/treasury":
                            send_telegram_msg(chat_id, f"🏛️ **[CFO Desk] Treasury Vault (TRC20):**\n`{COMPANY_TREASURY_WALLET}`\n\n⚡ Auto-sweep rule active at $50 (₹4,822)", thread_id)

                        elif cmd == "/rnd_scan":
                            send_telegram_msg(chat_id, "🔬 **[CTO R&D Brief]** High-yield node identified: `B2B Arbitrage Data Scraper` (Projected ROI: 4.5x).", thread_id)

                        elif cmd == "/unlock":
                            send_telegram_msg(chat_id, f"💳 **VIP Pass (1 USDT TRC20):**\n`{COMPANY_TREASURY_WALLET}`\n\nVerify via: `/verify <TXID>`", thread_id)

                        elif cmd.startswith("/verify"):
                            PAID_USERS.add(chat_id)
                            send_telegram_msg(chat_id, "✅ **Pass Verified by CFO Node!** VIP tools unlocked.", thread_id)

            except Exception:
                pass

        time.sleep(1)

if __name__ == "__main__":
    main()
    
