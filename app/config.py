"""
Configuration settings for the Yukuz Logistics Bot
"""

import os
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Bot configuration"""
    
    # Bot settings
    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")
    ADMINS: List[int] = Field(default_factory=list, env="ADMINS")
    CHANNEL_ID: Optional[int] = Field(None, env="CHANNEL_ID")
    
    # Database settings
    DATABASE_URL: str = Field("sqlite+aiosqlite:///./app/data.db", env="DATABASE_URL")
    
    # Application settings
    DEBUG: bool = Field(False, env="DEBUG")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Parse ADMINS from comma-separated string
        admins_str = os.getenv("ADMINS", "")
        if admins_str:
            try:
                self.ADMINS = [int(admin_id.strip()) for admin_id in admins_str.split(",") if admin_id.strip()]
            except ValueError:
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
