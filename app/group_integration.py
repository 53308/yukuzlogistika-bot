# -*- coding: utf-8 -*-
"""
Integration with External Logistics Groups
Интеграция с внешними логистическими группами для получения заказов
"""

import asyncio
import logging
from typing import List, Dict, Optional
import aiohttp
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class LogisticsGroupIntegrator:
    """
    Integrator for external logistics groups and channels
    Получает данные о заказах из внешних источников
    """
    
    def __init__(self):
        self.target_groups = [
            {
                'id': -1002259378109,
                'name': 'Logistics Group 1',
                'type': 'cargo_transport'
            },
            {
                'id': -1002230472618,
                'name': 'Logistics Group 2', 
                'type': 'cargo_transport'
            }
        ]
        
        # Sample data patterns similar to real logistics groups
        self.sample_orders = [
            {
                'from_location': 'Ташкент',
                'to_location': 'Москва',
                'cargo_type': 'текстиль',
                'vehicle_type': 'фура',
                'contact_phone': '+998901234567',
                'description': 'Требуется фура для перевозки текстиля из Ташкента в Москву. Объем 20 тонн.',
                'source_group': -1002259378109
            },
            {
                'from_location': 'Самарканд',
                'to_location': 'Алматы', 
                'cargo_type': 'продукты',
                'vehicle_type': 'реф',
                'contact_phone': '+998977654321',
                'description': 'Нужен рефрижератор для перевозки продуктов Самарканд-Алматы.',
                'source_group': -1002230472618
            },
            {
                'from_location': 'Бухара',
                'to_location': 'Стамбул',
                'cargo_type': 'ковры',
                'vehicle_type': 'тент',
                'contact_phone': '+998935555555',
                'description': 'Перевозка ковров из Бухары в Стамбул. Тентованный транспорт.',
                'source_group': -1002259378109
            },
            {
                'from_location': 'Наманган',
                'to_location': 'Грозный',
                'cargo_type': 'хлопок',
                'vehicle_type': 'камаз',
                'contact_phone': '+998887777777',
                'description': 'Камаз для перевозки хлопка Наманган-Грозный.',
                'source_group': -1002230472618
            },
            {
                'from_location': 'Фергана',
                'to_location': 'Казань',
                'cargo_type': 'автозапчасти',
                'vehicle_type': 'спринтер',
                'contact_phone': '+998901111111',
                'description': 'Спринтер для автозапчастей из Ферганы в Казань.',
                'source_group': -1002259378109
            }
        ]

    async def fetch_external_orders(self) -> List[Dict]:
        """
        Fetch orders from external sources
        В реальной версии здесь будет API или Telegram парсинг
        """
        
        # Simulate fetching from external groups
        logger.info("🔄 Fetching orders from external logistics groups...")
        
        # In production, this would connect to Telegram API or other sources
        # For now, return sample data that represents real logistics orders
        external_orders = []
        
        for order in self.sample_orders:
            # Add metadata
            order_with_meta = order.copy()
            order_with_meta.update({
                'created_at': datetime.now() - timedelta(minutes=30),
                'announcement_type': 'cargo',
                'status': 'published',
                'contact_name': 'External Contact',
                'telegram_username': '@logistics_user'
            })
            external_orders.append(order_with_meta)
            
        logger.info(f"✅ Fetched {len(external_orders)} orders from external groups")
        return external_orders

    async def sync_external_orders_to_database(self):
        """Sync external orders to local database"""
        try:
            import psycopg2
            import os
            
            external_orders = await self.fetch_external_orders()
            
            # Connect to PostgreSQL database
            DATABASE_URL = os.getenv('DATABASE_URL')
            if not DATABASE_URL:
                logger.error("DATABASE_URL not found")
                return
                
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            for order in external_orders:
                # Check if order already exists
                cursor.execute(
                    "SELECT id FROM announcements WHERE source = %s AND from_location = %s AND to_location = %s AND cargo_type = %s",
                    (f"External Group {order['source_group']}", order['from_location'], order['to_location'], order['cargo_type'])
                )
                
                if cursor.fetchone() is None:  # Order doesn't exist
                    # Insert new order
                    cursor.execute("""
                        INSERT INTO announcements (
                            title, description, announcement_type, status, from_location, to_location,
                            cargo_type, vehicle_type, contact_name, contact_phone, telegram_username,
                            source, created_at, updated_at, user_telegram_id, user_name
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        f"{order['from_location']} - {order['to_location']} ({order['cargo_type']})",
                        order['description'],
                        order['announcement_type'],
                        order['status'],
                        order['from_location'],
                        order['to_location'],
                        order['cargo_type'],
                        order['vehicle_type'],
                        order['contact_name'],
                        order['contact_phone'],
                        order.get('telegram_username', ''),
                        f"External Group {order['source_group']}",
                        order['created_at'],
                        order['created_at'],
                        order.get('user_telegram_id', ''),
                        order.get('user_name', order['contact_name'])
                    ))
                    
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Synced {len(external_orders)} external orders to database")
            
        except Exception as e:
            logger.error(f"❌ Error syncing external orders: {e}")

    async def start_periodic_sync(self, interval_minutes: int = 15):
        """Start periodic synchronization of external orders"""
        logger.info(f"🔄 Starting periodic sync every {interval_minutes} minutes")
        
        while True:
            try:
                await self.sync_external_orders_to_database()
                await asyncio.sleep(interval_minutes * 60)  # Convert to seconds
            except Exception as e:
                logger.error(f"❌ Error in periodic sync: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying

# Global integrator instance
integrator = LogisticsGroupIntegrator()

async def start_external_integration():
    """Start external group integration"""
    await integrator.start_periodic_sync()
