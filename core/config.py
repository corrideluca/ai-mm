"""Configuration and risk limits."""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class RiskLimits:
    max_bet_pct: float = float(os.getenv("MAX_BET_PCT", "0.20"))  # max 20% of balance per trade
    daily_loss_pct: float = float(os.getenv("DAILY_LOSS_PCT", "0.30"))  # stop if 30% of balance lost in a day
    max_position_pct: float = float(os.getenv("MAX_POSITION_PCT", "0.50"))  # max 50% in one market


@dataclass
class Config:
    # Polymarket
    private_key: str = os.getenv("POLYMARKET_PRIVATE_KEY", "")
    api_key: str = os.getenv("POLYMARKET_API_KEY", "")
    api_secret: str = os.getenv("POLYMARKET_API_SECRET", "")
    api_passphrase: str = os.getenv("POLYMARKET_API_PASSPHRASE", "")
    funder_address: str = os.getenv("POLYMARKET_FUNDER_ADDRESS", "")
    chain_id: int = int(os.getenv("CHAIN_ID", "137"))
    clob_url: str = "https://clob.polymarket.com"

    # Risk
    risk: RiskLimits = field(default_factory=RiskLimits)

    # Cache
    cache_ttl_seconds: int = 300  # 5 minutes


config = Config()
