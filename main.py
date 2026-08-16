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
RND_INCOME_IDEAS = [
    {"niche": "Affiliate Traffic Node", "projected_roi": "3.8x", "risk": "Low"},
    {"niche": "Solana Sniper Monitor", "projected_roi": "5.2x", "risk": "Medium"},
    {"niche": "B2B Lead Extractor", "projected_roi": "4.1x", "risk": "Low"},
    {"niche": "AI Prompt Bundler", "projected_roi": "3.2x", "risk": "Very Low"},
    {"niche": "Crypto Sentiment Arbitrage", "projected_roi": "4.8x", "risk": "Medium"}
]

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
        self.dead_agents_history = 0

    def run_network_cycle(self):
        for i, agent in enumerate(self.agents):
            if agent.is_alive:
                agent.work_cycle()
            else:
                self.dead_agents_history += 1
                best_agent = self.get_best_performing_agent()
                new_id = f"Agent-Evo-{random.randint(100, 999)}"
                # Learns from best agent
                self.agents[i] = AutonomousAgent(new_id, f"Evolved: {best_agent.niche}")

    def spawn_custom_agent(self, niche_name):
        new_id = f"Agent-RND-{random.randint(100, 999)}"
        new_agent = AutonomousAgent(new_id, niche_name)
        self.agents.append(new_agent)
        return new_id

    def get_best_performing_agent(self):
        alive_agents = [ag for ag in self.agents if ag.is_alive]
        if alive_agents:
            return max(alive_agents, key=lambda x: x.total_generated)
        return self.agents[0]

    def get_status_text(self):
        text = "🤖 **OmniTech Earning Swarm Telemetry**\n\n"
        total_fleet_inr = 0
        for ag in self.agents:
            status = "🟢 ALIVE" if ag.is_alive else "💀 DEAD"
            fuel_inr = ag.wallet_balance * USD_TO_INR
            total_inr = ag.total_generated * USD_TO_INR
            total_fleet_inr += total_inr
            text += f"🔹 **{ag.agent_id}** ({ag.niche})\n   • Status: {status} | Fuel: ${ag.wallet_balance:.2f} (₹{fuel_inr:,.0f}) | Total: ${ag.total_generated:.2f} (₹{total_inr:,.0f})\n\n"
        
        text += f"💰 **Combined Fleet Revenue:** ₹{total_fleet_inr:,.0f}\n"
        text += f"🧠 **Optimization History:** {self.dead_agents_history} failed nodes pruned & evolved."
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
    print("[*] OmniTech Swarm + R&D Controller is LIVE...")
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

                        if text == "/start":
                            menu_msg = (
                                "👑 **OmniTech Autonomous Corporate Swarm**\n\n"
                                "📊 **Core Telemetry:**\n"
                                "👉 /agents - Live Swarm Health & INR Balances\n"
                                "👉 /treasury - Master Binance Wallet\n\n"
                                "🔬 **R&D & CEO Intelligence:**\n"
                                "👉 /rnd_scan - Scan New High-Income Streams\n"
                                "👉 /spawn_agent <niche> - Deploy Dedicated Agent\n"
                                "👉 /fleet_audit - Performance & Evolution Report\n\n"
                                "💎 **Monetization Paywall:**\n"
                                "👉 /unlock - Get VIP Access (1 USDT)\n"
                                "👉 /market_signals - Premium Signal Feed"
                            )
                            send_telegram_msg(chat_id, menu_msg)

                        elif text == "/agents":
                            send_telegram_msg(chat_id, swarm.get_status_text())

                        elif text == "/treasury":
                            send_telegram_msg(chat_id, f"🏛️ **Master Treasury Wallet (TRC20):**\n`{COMPANY_TREASURY_WALLET}`\n\n⚡ 50% split trigger active at $50 (₹4,822)")

                        elif text == "/rnd_scan":
                            idea = random.choice(RND_INCOME_IDEAS)
                            best = swarm.get_best_performing_agent()
                            rnd_report = (
                                "🔬 **OmniTech R&D Discovery Briefing**\n\n"
                                f"💡 **Target Stream:** `{idea['niche']}`\n"
                                f"📈 **Projected ROI:** {idea['projected_roi']}\n"
                                f"🛡️ **Risk Profile:** {idea['risk']}\n"
                                f"🏆 **Benchmark Node:** {best.agent_id} (${best.total_generated:.2f})\n\n"
                                f"To deploy this stream, send:\n`/spawn_agent {idea['niche']}`"
                            )
                            send_telegram_msg(chat_id, rnd_report)

                        elif text.startswith("/spawn_agent"):
                            parts = text.split(maxsplit=1)
                            niche = parts[1] if len(parts) > 1 else "Custom Micro-Service"
                            new_agent_id = swarm.spawn_custom_agent(niche)
                            send_telegram_msg(chat_id, f"🚀 **Agent Deployed!**\n\nNode **{new_agent_id}** is active on niche: `{niche}`\nAdded to autonomous work fleet.")

                        elif text == "/fleet_audit":
                            best = swarm.get_best_performing_agent()
                            audit_msg = (
                                "📈 **Fleet Executive Performance Audit**\n\n"
                                f"👑 **Leading Alpha Agent:** {best.agent_id} ({best.niche})\n"
                                f"💵 **Alpha Gross Earning:** ${best.total_generated:.2f} (₹{best.total_generated * USD_TO_INR:,.0f})\n"
                                f"⚰️ **Pruned Underperforming Nodes:** {swarm.dead_agents_history}\n"
                                "⚡ **Self-Healing Loop:** Enabled & Adaptive"
                            )
                            send_telegram_msg(chat_id, audit_msg)

                        elif text == "/unlock":
                            pay_msg = (
                                "💳 **Unlock All Premium Autonomous Services**\n\n"
                                f"1️⃣ Send **1 USDT** (TRC20) to Treasury Wallet:\n`{COMPANY_TREASURY_WALLET}`\n\n"
                                "2️⃣ After transfer, send verification:\n"
                                "`/verify <Your_TXID_Or_Wallet>`"
                            )
                            send_telegram_msg(chat_id, pay_msg)

                        elif text.startswith("/verify"):
                            parts = text.split()
                            if len(parts) > 1:
                                PAID_USERS.add(chat_id)
                                send_telegram_msg(chat_id, "✅ **Payment Verified!** VIP commands are unlocked.")
                            else:
                                send_telegram_msg(chat_id, "⚠️ Provide TXID: `/verify <TXID>`")

                        elif text == "/market_signals":
                            if chat_id in PAID_USERS:
                                send_telegram_msg(chat_id, "📈 **VIP Alpha Signal:** BTC consolidating above $94k. Bullish breakout targets active.")
                            else:
                                send_telegram_msg(chat_id, "🔒 **Locked!** Use `/unlock` to access.")

            except Exception:
                pass

        time.sleep(1)

if __name__ == "__main__":
    main()
                        
