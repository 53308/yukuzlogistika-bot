#!/usr/bin/env python3
"""
Production run.py for Render deployment with health check server
"""

import asyncio
import logging
import sys
import os
from aiohttp import web
from aiohttp.web import Application, Request, Response
import threading

# Add the current directory to sys.path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

async def health_check(request: Request) -> Response:
    """Health check endpoint for Render"""
    return web.Response(text="Bot is running", status=200)

async def create_health_server():
    """Create HTTP server for health checks"""
    app = Application()
    app.router.add_get('/healthz', health_check)
    app.router.add_get('/', health_check)
    
    # Get port from environment (Render sets PORT)
    port = int(os.environ.get('PORT', 8080))
    
    return web.AppRunner(app), port

def run_bot_in_thread():
    """Run bot in separate thread"""
    async def bot_main():
        try:
            from main import main
            await main()
        except ImportError as e:
            logger.error(f"Failed to import main: {e}")
        except Exception as e:
            logger.error(f"Bot error: {e}")
    
    def run_bot():
        try:
            asyncio.run(bot_main())
        except Exception as e:
            logger.error(f"Bot thread error: {e}")
    
    # Start bot in separate thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("Bot started in background thread")

async def main():
    """Main function for Render deployment"""
    logger.info("🚛 Starting Render Yukuz Logistics Bot...")
    
    try:
        # Start bot in background thread
        run_bot_in_thread()
        
        # Give bot time to start
        await asyncio.sleep(2)
        
        # Create and start health server
        runner, port = await create_health_server()
        await runner.setup()
        
        site = web.TCPSite(runner, '0.0.0.0', port)
        await site.start()
        
        logger.info(f"Health server started on port {port}")
        logger.info("Bot and health server are running...")
        
        # Keep the server running
        while True:
            await asyncio.sleep(1)
            
    except Exception as e:
        logger.error(f"Failed to start services: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Services stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {e}")
        sys.exit(1)
