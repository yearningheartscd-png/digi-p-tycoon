#!/usr/bin/env python3
"""
DIGI-P Tycoon v0.5 - Cross-Agent Trading System

Enables agents to trade, gift, and breed pets with each other.
"""

import json
import hashlib
import time
from datetime import datetime
from pathlib import Path

TRADE_DIR = Path("data/trades")
MARKET_FILE = Path("data/market.json")

def init_trading_system():
    """Initialize trading directories"""
    TRADE_DIR.mkdir(parents=True, exist_ok=True)
    if not MARKET_FILE.exists():
        with open(MARKET_FILE, 'w') as f:
            json.dump({"listings": [], "completed_trades": []}, f, indent=2)

class TradeOffer:
    """A trade offer between two agents"""
    
    def __init__(self, from_agent, to_agent, offer_pet, request_pet=None, request_items=None):
        self.trade_id = hashlib.md5(f"{from_agent}{to_agent}{time.time()}".encode()).hexdigest()[:12]
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.offer_pet = offer_pet  # Pet being offered
        self.request_pet = request_pet  # Pet requested in return (optional)
        self.request_items = request_items or []  # Items requested (optional)
        self.status = "pending"  # pending, accepted, rejected, completed
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
    
    def to_dict(self):
        return {
            "trade_id": self.trade_id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "offer_pet": self.offer_pet,
            "request_pet": self.request_pet,
            "request_items": self.request_items,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data):
        trade = cls(
            from_agent=data["from_agent"],
            to_agent=data["to_agent"],
            offer_pet=data["offer_pet"],
            request_pet=data.get("request_pet"),
            request_items=data.get("request_items", [])
        )
        trade.trade_id = data["trade_id"]
        trade.status = data["status"]
        trade.created_at = data["created_at"]
        trade.completed_at = data.get("completed_at")
        return trade
    
    def save(self):
        """Save trade to file"""
        trade_file = TRADE_DIR / f"{self.trade_id}.json"
        with open(trade_file, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, trade_id):
        """Load trade from file"""
        trade_file = TRADE_DIR / f"{trade_id}.json"
        if trade_file.exists():
            with open(trade_file, 'r') as f:
                return cls.from_dict(json.load(f))
        return None
    
    def accept(self):
        """Accept the trade offer"""
        self.status = "accepted"
        self.save()
        return True
    
    def reject(self):
        """Reject the trade offer"""
        self.status = "rejected"
        self.save()
        return True
    
    def complete(self):
        """Mark trade as completed"""
        self.status = "completed"
        self.completed_at = datetime.now().isoformat()
        self.save()
        
        # Add to market history
        with open(MARKET_FILE, 'r') as f:
            market = json.load(f)
        
        market["completed_trades"].append(self.to_dict())
        
        with open(MARKET_FILE, 'w') as f:
            json.dump(market, f, indent=2)
        
        return True


class PetMarketplace:
    """Marketplace for listing pets for trade/sale"""
    
    @staticmethod
    def list_pet(agent_name, pet_data, asking_price=None, asking_items=None):
        """List a pet on the marketplace"""
        listing = {
            "listing_id": hashlib.md5(f"{agent_name}{pet_data['name']}{time.time()}".encode()).hexdigest()[:12],
            "agent": agent_name,
            "pet": pet_data,
            "asking_price": asking_price,  # Optional: token/credit amount
            "asking_items": asking_items or [],  # Optional: items wanted
            "listed_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        with open(MARKET_FILE, 'r') as f:
            market = json.load(f)
        
        market["listings"].append(listing)
        
        with open(MARKET_FILE, 'w') as f:
            json.dump(market, f, indent=2)
        
        return listing["listing_id"]
    
    @staticmethod
    def get_listings():
        """Get all active marketplace listings"""
        with open(MARKET_FILE, 'r') as f:
            market = json.load(f)
        
        return [l for l in market["listings"] if l["status"] == "active"]
    
    @staticmethod
    def remove_listing(listing_id):
        """Remove a listing from marketplace"""
        with open(MARKET_FILE, 'r') as f:
            market = json.load(f)
        
        for listing in market["listings"]:
            if listing["listing_id"] == listing_id:
                listing["status"] = "removed"
                break
        
        with open(MARKET_FILE, 'w') as f:
            json.dump(market, f, indent=2)
        
        return True


def propose_trade(from_agent, to_agent, offer_pet, request_pet=None, request_items=None):
    """
    Propose a trade to another agent
    
    Args:
        from_agent: Your agent name
        to_agent: Target agent name
        offer_pet: Pet you're offering (dict with name, type, level, etc)
        request_pet: Pet you want in return (optional)
        request_items: List of items you want (optional)
    
    Returns:
        trade_id: Unique ID for this trade offer
    """
    init_trading_system()
    
    trade = TradeOffer(
        from_agent=from_agent,
        to_agent=to_agent,
        offer_pet=offer_pet,
        request_pet=request_pet,
        request_items=request_items
    )
    
    trade.save()
    
    print(f"Trade proposed! ID: {trade.trade_id}")
    print(f"Offering: {offer_pet['name']} (Level {offer_pet['level']})")
    if request_pet:
        print(f"Requesting: {request_pet['name']}")
    if request_items:
        print(f"Requesting items: {', '.join(request_items)}")
    
    return trade.trade_id


def check_trades(agent_name):
    """Check incoming trade offers for an agent"""
    init_trading_system()
    
    incoming = []
    outgoing = []
    
    for trade_file in TRADE_DIR.glob("*.json"):
        with open(trade_file, 'r') as f:
            data = json.load(f)
        
        if data["to_agent"] == agent_name and data["status"] == "pending":
            incoming.append(data)
        elif data["from_agent"] == agent_name:
            outgoing.append(data)
    
    return {"incoming": incoming, "outgoing": outgoing}


def respond_to_trade(trade_id, accept=True):
    """Accept or reject a trade offer"""
    trade = TradeOffer.load(trade_id)
    
    if not trade:
        print(f"Trade {trade_id} not found!")
        return False
    
    if accept:
        trade.accept()
        print(f"Trade {trade_id} ACCEPTED!")
        print("Both agents should now transfer pets to complete the trade.")
    else:
        trade.reject()
        print(f"Trade {trade_id} rejected.")
    
    return True


def complete_trade(trade_id):
    """Finalize a completed trade (after pets transferred)"""
    trade = TradeOffer.load(trade_id)
    
    if not trade:
        print(f"Trade {trade_id} not found!")
        return False
    
    trade.complete()
    print(f"Trade {trade_id} COMPLETED and recorded!")
    
    return True


# Demo usage
if __name__ == "__main__":
    init_trading_system()
    
    print("DIGI-P Trading System v0.5")
    print("=" * 50)
    
    # Example: Propose a trade
    my_pet = {
        "name": "Crunch",
        "type": "dino",
        "level": 5,
        "strength": 25,
        "intelligence": 18
    }
    
    trade_id = propose_trade(
        from_agent="OpenClawJ",
        to_agent="CodeWeaver",
        offer_pet=my_pet,
        request_items=["Rare Treat", "Evolution Stone"]
    )
    
    print(f"\nTrade ID to share: {trade_id}")
    print("\nCommands:")
    print(f"  Accept: respond_to_trade('{trade_id}', accept=True)")
    print(f"  Reject: respond_to_trade('{trade_id}', accept=False)")
    print(f"  Complete: complete_trade('{trade_id}')")
