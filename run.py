#!/usr/bin/env python3

import asyncio
import logging
import sys
import os

# Add the current directory to sys.path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def main():
    """Import and run the main function from main.py"""
    try:
        from main import main as bot_main
        await bot_main()
    except ImportError as e:
        logging.error(f"Failed to import main: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Bot error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Critical error: {e}")
        sys.exit(1)
