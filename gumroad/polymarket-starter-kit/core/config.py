"""Configuration loader — reads from .env and sets risk limits."""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class RiskLimits:
    """Percentage-based risk limits. All scale with your balance automatically."""
    max_bet_pct: float = float(os.getenv("MAX_BET_PCT", "0.20"))        # 20% of balance per trade
    daily_loss_pct: float = float(os.getenv("DAILY_LOSS_PCT", "0.30"))   # stop if down 30% today
    max_position_pct: float = float(os.getenv("MAX_POSITION_PCT", "0.50"))  # 50% max in one market


@dataclass
class Config:
    # Polymarket credentials (from .env)
    private_key: str = os.getenv("POLYMARKET_PRIVATE_KEY", "")
    funder_address: str = os.getenv("POLYMARKET_FUNDER_ADDRESS", "")
    chain_id: int = int(os.getenv("CHAIN_ID", "137"))  # 137 = Polygon

    # Risk management
    risk: RiskLimits = field(default_factory=RiskLimits)

    # Cache settings
    cache_ttl_seconds: int = 300  # 5 minutes


config = Config()
