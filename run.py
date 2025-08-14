"""
Entry point for Yukuz Logistics Bot on Render
Handles HTTP server for health checks and runs Telegram bot
"""

import asyncio
import logging
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    """HTTP handler for health checks and status"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Yukuz Logistics Bot</title>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #333; text-align: center; }
                    .status { background: #e8f5e8; padding: 15px; border-radius: 5px; border-left: 4px solid #4caf50; }
                    .info { margin: 20px 0; line-height: 1.6; }
                    .bot-info { background: #e3f2fd; padding: 15px; border-radius: 5px; border-left: 4px solid #2196f3; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚛 Yukuz Logistics Bot</h1>
                    
                    <div class="status">
                        <strong>✅ Status: Online</strong><br>
                        Bot is running and ready to accept connections.
                    </div>
                    
                    <div class="info">
                        <h3>📦 About</h3>
                        <p>Yukuz Logistics Bot - это Telegram бот для размещения объявлений о грузах и транспорте в Узбекистане.</p>
                        
                        <h3>🔧 Features</h3>
                        <ul>
                            <li>📦 Создание объявлений о грузах</li>
                            <li>🚛 Создание объявлений о транспорте</li>
                            <li>🔍 Поиск объявлений</li>
                            <li>👨‍💼 Админ панель</li>
                            <li>🌐 Поддержка узбекского и русского языков</li>
                        </ul>
                    </div>
                    
                    <div class="bot-info">
                        <strong>🤖 Telegram Bot:</strong><br>
                        @yukuzlogistika_bot
                    </div>
                </div>
            </body>
            </html>
            """
            
            self.wfile.write(html.encode())
            
        elif self.path in ['/health', '/healthz']:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = '{"status": "healthy", "service": "yukuz-logistics-bot"}'
            self.wfile.write(response.encode())
            
        else:
            self.send_error(404, "Not Found")
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info(f"HTTP {format % args}")


def run_http_server():
    """Run HTTP server for health checks"""
    port = int(os.getenv('PORT', 10000))
    
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    
    logger.info(f"HTTP server starting on http://0.0.0.0:{port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("HTTP server stopped")
        httpd.shutdown()


def run_bot():
    """Run the Telegram bot"""
    try:
        # Import the main function from app.main
        from app.main import main
        logger.info("Starting Telegram bot...")
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        import time
        time.sleep(5)
        run_bot()  # Restart bot


def main():
    """Main function - runs both HTTP server and Telegram bot"""
    logger.info("🚛 Starting Yukuz Logistics Bot on Render...")
    
    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # Run the bot in the main thread
    run_bot()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application crashed: {e}")
        sys.exit(1)
