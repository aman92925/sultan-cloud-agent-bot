import os
import time
import random
import requests

# Render ke Environment Variables se token fetch hoga
TELEGRAM_TOKEN = os.getenv("MINING_BOT_TOKEN")

# Aapka Binance TRC20 Wallet Address
COMPANY_TREASURY_WALLET = "TEnk27LNfmBKytkXTXeWcY3zWHVgMfw96p"
REVENUE_THRESHOLD = 50.0  
SPLIT_PERCENTAGE = 0.50

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

        self.wallet_balance -= 0.50
        earned = round(random.uniform(0.5, 3.5), 2)
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
            AutonomousAgent("Agent-Gamma", "Code Quality Auditor")
        ]

    def run_network_cycle(self):
        for i, agent in enumerate(self.agents):
            if agent.is_alive:
                agent.work_cycle()
            else:
                new_id = f"Agent-{random.randint(100, 999)}"
                self.agents[i] = AutonomousAgent(new_id, agent.niche)

    def get_status_text(self):
        text = "🤖 **OmniTech Autonomous Telemetry**\n\n"
        for ag in self.agents:
            status = "🟢 ALIVE" if ag.is_alive else "💀 DEAD"
            text += f"🔹 **{ag.agent_id}** ({ag.niche})\n   • Status: {status}\n   • Fuel: ${ag.wallet_balance:.2f}\n   • Total: ${ag.total_generated:.2f}\n\n"
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
    print("[*] OmniTechAutoEarning Swarm is running in Cloud...")
    last_update_id = 0
    last_cycle_time = time.time()

    while True:
        # Har 20 second mein swarm cycle
        if time.time() - last_cycle_time > 20:
            swarm.run_network_cycle()
            last_cycle_time = time.time()

        # Telegram polling logic
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

                        if text == "/start":
                            send_telegram_msg(chat_id, "👑 **OmniTech Auto Earning Command Center**\n\nBot: @OmniTechautoearningBot\n\nCommands:\n👉 /agents - Live Swarm Telemetry\n👉 /treasury - Master Binance Wallet\n👉 /force_work - Instant Cycle Run")
                        elif text == "/agents":
                            send_telegram_msg(chat_id, swarm.get_status_text())
                        elif text == "/treasury":
                            send_telegram_msg(chat_id, f"🏛️ **Treasury Wallet (Binance TRC20):**\n`{COMPANY_TREASURY_WALLET}`\n\n⚡ 50% split trigger active at ${REVENUE_THRESHOLD}")
                        elif text == "/force_work":
                            swarm.run_network_cycle()
                            send_telegram_msg(chat_id, "⚡ Manual cycle executed across all swarm nodes.")
            except Exception:
                pass

        time.sleep(1)

if __name__ == "__main__":
    main()
          
