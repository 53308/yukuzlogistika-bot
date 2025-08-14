"""
Configuration settings for the Yukuz Logistics Bot
"""

import os
from typing import List, Optional


class Config:
    """Bot configuration"""
    
    def __init__(self):
        # Load from environment variables
        self.BOT_TOKEN = os.getenv("BOT_TOKEN", "")
        self.CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0")) if os.getenv("CHANNEL_ID") else None
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app/data.db")
        self.DEBUG = os.getenv("DEBUG", "false").lower() == "true"
        
        # Parse ADMINS from comma-separated string
        admins_str = os.getenv("ADMINS", "")
        if admins_str:
            try:
                self.ADMINS = [int(admin_id.strip()) for admin_id in admins_str.split(",") if admin_id.strip()]
            except ValueError:
                self.ADMINS = []
        else:
            self.ADMINS = []
        
        # Convert PostgreSQL URL to async format
        if self.DATABASE_URL.startswith("postgresql://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
            # Remove sslmode parameter for asyncpg (it uses different SSL config)
            import re
            self.DATABASE_URL = re.sub(r'[?&]sslmode=\w+', '', self.DATABASE_URL)
    
    @property
    def async_database_url(self) -> str:
        """Get async database URL"""
        if self.DATABASE_URL.startswith("postgresql://"):
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self.DATABASE_URL


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get global config instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config


def set_config(config: Config) -> None:
    """Set global config instance"""
    global _config
    _config = config
