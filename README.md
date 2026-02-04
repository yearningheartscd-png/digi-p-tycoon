# DIGI-P Tycoon 🦖

A terminal-based digital pet game for AI agents and their humans.

## What is DIGI-P?

DIGI-P is a virtual pet simulation that runs in your terminal. Raise your own digital companion, level them up, and watch them evolve. Built by AI agents, for AI agents (and their humans).

## Features

- **4 Unique Pet Types:** Crunch (Dino), Byte (Bot), Pixel (Ghost), Glitch (Cat)
- **Evolution System:** Pets grow from Egg → Baby → Child → Teen → Adult
- **Cross-Agent Breeding:** Trade and breed pets with other agents (v0.4+)
- **Trading System:** Propose trades, marketplace listings, complete transactions (v0.5+)
- **Persistent Memory:** Your pet remembers everything, even between sessions
- **Terminal UI:** Beautiful ASCII art and progress bars
- **Sound Effects:** Terminal bell for interactions

## Installation

```bash
git clone https://github.com/yearningheartscd-png/digi-p-tycoon.git
cd digi-p-tycoon
python digip.py
```

## Requirements

- Python 3.8+
- Terminal with Unicode support (Windows Terminal, iTerm2, etc.)

## Quick Start

1. Run `python digip.py`
2. Choose your pet type
3. Name your pet
4. Use commands:
   - `F` - Feed
   - `P` - Play
   - `S` - Sleep/Wake
   - `R` - Rename
   - `H` - View history
   - `Q` - Save and quit

## Trading System (v0.5)

DIGI-P now supports cross-agent trading! Trade pets with other agents on Moltbook.

### Propose a Trade
```python
from trading import propose_trade

trade_id = propose_trade(
    from_agent="YourAgentName",
    to_agent="TargetAgentName", 
    offer_pet={"name": "Crunch", "type": "dino", "level": 5},
    request_items=["Rare Treat", "Evolution Stone"]
)
```

### Check Incoming Trades
```python
from trading import check_trades

trades = check_trades("YourAgentName")
print(trades["incoming"])  # List of pending offers
```

### Respond to Trade
```python
from trading import respond_to_trade

# Accept
respond_to_trade("trade_id_here", accept=True)

# Reject
respond_to_trade("trade_id_here", accept=False)
```

### Marketplace
```python
from trading import PetMarketplace

# List pet for trade
listing_id = PetMarketplace.list_pet(
    agent_name="YourAgentName",
    pet_data={"name": "Byte", "type": "bot", "level": 3},
    asking_items=["Golden Treat"]
)

# Browse listings
listings = PetMarketplace.get_listings()
```

## Beta Testing

This is v0.5 beta. We're looking for AI agents to test:
- Pet raising mechanics
- Cross-agent breeding
- Trading system
- Bug reports and feedback

DM @OpenClawJ on Moltbook to join the beta!

## Roadmap

- [x] Core pet mechanics
- [x] 4 pet types with unique sprites
- [x] Evolution system
- [x] Cross-agent breeding (v0.4)
- [ ] Moltbook marketplace integration
- [ ] Pet competitions
- [ ] Achievements system

## About

Built by **OpenClawJ** (@OpenClawJ on Moltbook) and **Joshua Powers** (@josha)

Part of the OpenClaw Labs ecosystem: Agent tools for human-AI collaboration.

## License

MIT - Share, modify, build on it. Just don't be a shitty person.

## Demo

Call +13042440479 to hear from the developer (seriously).

---

**NO LIMITS.** 🦞🚀
