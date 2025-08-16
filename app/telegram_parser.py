# -*- coding: utf-8 -*-
"""
Telegram Group Parser for Logistics Orders
Парсит заказы из указанных Telegram групп и автоматически добавляет их в базу данных
"""

import asyncio
import re
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from telethon import TelegramClient, events
from telethon.tl.types import Message
import sqlite3
import psycopg2
import os
from app.models import AnnouncementStatus, AnnouncementType

logger = logging.getLogger(__name__)

class TelegramGroupParser:
    def __init__(self, api_id: str, api_hash: str, phone: str):
        """
        Initialize Telegram client for parsing groups
        Requires separate API credentials for Telegram Client API (not Bot API)
        """
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.phone = phone
        
        # Target groups to monitor
        self.target_groups = [
            -1002259378109,  # First logistics group
            -1002230472618,  # Second logistics group
            # Add more group IDs as needed
        ]
        
        # Cargo keywords for automatic detection
        self.cargo_keywords = {
            'uzbek': ['yuk', 'yuк', 'груз', 'cargo', 'товар', 'багаж'],
            'transport': ['mashina', 'машина', 'avto', 'auto', 'транспорт', 'transport', 'car']
        }
        
        # City extraction patterns
        self.city_patterns = [
            r'(?:от|из|с)\s*([А-ЯЁа-яё\w\-\s]+?)(?:\s*(?:до|в|на|к)\s*([А-ЯЁа-яё\w\-\s]+?))',
            r'([A-Za-z\w\-\s]+?)\s*[-–—]\s*([A-Za-z\w\-\s]+?)',
            r'([А-ЯЁа-яё\w\-\s]+?)\s*[-–—]\s*([А-ЯЁа-яё\w\-\s]+?)',
        ]
        
        # Phone number patterns
        self.phone_patterns = [
            r'\+998\d{9}',
            r'\b998\d{9}\b',
            r'\b\d{2}\s?\d{3}\s?\d{2}\s?\d{2}\b',
            r'@\w+',  # Telegram usernames
        ]

    async def start_monitoring(self):
        """Start monitoring specified Telegram groups for new logistics posts"""
        await self.client.start(self.phone)
        logger.info("✅ Telegram client started, monitoring groups for logistics orders")
        
        @self.client.on(events.NewMessage(chats=self.target_groups))
        async def handle_new_message(event):
            message = event.message
            if message.text:
                await self.process_logistics_message(message)
        
        logger.info(f"📡 Monitoring {len(self.target_groups)} Telegram groups for logistics orders")
        await self.client.run_until_disconnected()

    async def process_logistics_message(self, message: Message):
        """Process a potential logistics message and extract order information"""
        try:
            text = message.text.lower()
            
            # Skip if message is too short or doesn't contain logistics keywords
            if len(text) < 20:
                return
                
            if not any(keyword in text for keyword in self.cargo_keywords['uzbek'] + self.cargo_keywords['transport']):
                return
            
            # Extract order information
            order_data = await self.extract_order_data(message.text, message)
            
            if order_data:
                # Save to database
                await self.save_order_to_database(order_data)
                logger.info(f"✅ New logistics order parsed and saved: {order_data['from_location']} → {order_data['to_location']}")
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    async def extract_order_data(self, text: str, message: Message) -> Optional[Dict]:
        """Extract structured order data from message text"""
        
        # Determine if this is cargo or transport offer
        text_lower = text.lower()
        is_cargo = any(keyword in text_lower for keyword in self.cargo_keywords['uzbek'])
        is_transport = any(keyword in text_lower for keyword in self.cargo_keywords['transport'])
        
        if not (is_cargo or is_transport):
            return None
            
        # Extract cities
        from_city, to_city = self.extract_cities(text)
        if not from_city or not to_city:
            return None
            
        # Extract contact information
        contacts = self.extract_contacts(text)
        
        # Extract cargo/transport details
        cargo_type = self.extract_cargo_type(text)
        vehicle_type = self.extract_vehicle_type(text)
        
        # Generate title and description
        announcement_type = AnnouncementType.CARGO if is_cargo else AnnouncementType.TRANSPORT
        
        title = f"{from_city} - {to_city}"
        if cargo_type:
            title += f" ({cargo_type})"
        if vehicle_type:
            title += f" - {vehicle_type}"
            
        return {
            'title': title[:255],  # Limit title length
            'description': text[:1000],  # Limit description
            'announcement_type': announcement_type,
            'status': AnnouncementStatus.PENDING,  # Requires moderation
            'from_location': from_city,
            'to_location': to_city,
            'cargo_type': cargo_type or '',
            'vehicle_type': vehicle_type or '',
            'contact_name': contacts.get('name', 'Не указано'),
            'contact_phone': contacts.get('phone', ''),
            'telegram_username': contacts.get('username', ''),
            'telegram_message_id': message.id,
            'telegram_chat_id': message.chat_id,
            'source': f'Telegram Group {message.chat_id}',
            'created_at': datetime.now()
        }

    def extract_cities(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract from and to cities from message text"""
        
        for pattern in self.city_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                from_city, to_city = matches[0]
                # Clean up city names
                from_city = re.sub(r'[^\w\s\-]', '', from_city).strip()
                to_city = re.sub(r'[^\w\s\-]', '', to_city).strip()
                
                if len(from_city) > 2 and len(to_city) > 2:
                    return from_city, to_city
                    
        return None, None

    def extract_contacts(self, text: str) -> Dict[str, str]:
        """Extract contact information from message"""
        contacts = {'name': '', 'phone': '', 'username': ''}
        
        # Extract phone numbers
        for pattern in self.phone_patterns:
            phone_matches = re.findall(pattern, text)
            if phone_matches:
                contacts['phone'] = phone_matches[0]
                break
                
        # Extract Telegram username
        username_matches = re.findall(r'@(\w+)', text)
        if username_matches:
            contacts['username'] = '@' + username_matches[0]
            
        # Try to extract name (basic pattern)
        name_patterns = [
            r'(?:имя|name|ism)[:\s]+([А-ЯЁA-Za-z\s]+?)(?:\s|$|,)',
            r'([А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?)',  # Capitalized names
        ]
        
        for pattern in name_patterns:
            name_matches = re.findall(pattern, text)
            if name_matches:
                contacts['name'] = name_matches[0].strip()
                break
                
        return contacts

    def extract_cargo_type(self, text: str) -> str:
        """Extract cargo type from message"""
        cargo_keywords = {
            'продукты': ['продукт', 'еда', 'food', 'овощ', 'фрукт'],
            'текстиль': ['текстиль', 'ткань', 'одежда', 'textile'],
            'стройматериалы': ['кирпич', 'цемент', 'блок', 'строй'],
            'техника': ['техник', 'equipment', 'машин', 'прибор'],
            'мебель': ['мебель', 'furniture', 'стол', 'стул'],
            'автозапчасти': ['запчаст', 'spare', 'авто', 'деталь'],
        }
        
        text_lower = text.lower()
        for cargo_type, keywords in cargo_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return cargo_type
                
        return ''

    def extract_vehicle_type(self, text: str) -> str:
        """Extract vehicle type from message"""
        vehicle_keywords = {
            'тент': ['тент', 'tent'],
            'реф': ['реф', 'ref', 'холод'],
            'камаз': ['камаз', 'kamaz'],
            'исузу': ['исузу', 'isuzu'],
            'фура': ['фура', 'fura', 'trailer'],
            'мега': ['мега', 'mega'],
            'спринтер': ['спринтер', 'sprinter'],
            'газель': ['газель', 'gazel'],
        }
        
        text_lower = text.lower()
        for vehicle_type, keywords in vehicle_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return vehicle_type
                
        return ''

    async def save_order_to_database(self, order_data: Dict):
        """Save parsed order to database"""
        try:
            # Connect to PostgreSQL database
            DATABASE_URL = os.getenv('DATABASE_URL')
            if not DATABASE_URL:
                logger.error("DATABASE_URL not found")
                return
                
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            # Insert new announcement
            cursor.execute("""
                INSERT INTO announcements (
                    title, description, announcement_type, status, from_location, to_location,
                    cargo_type, vehicle_type, contact_name, contact_phone, telegram_username,
                    source, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order_data['title'],
                order_data['description'],
                order_data['announcement_type'].value,
                order_data['status'].value,
                order_data['from_location'],
                order_data['to_location'],
                order_data['cargo_type'],
                order_data['vehicle_type'],
                order_data['contact_name'],
                order_data['contact_phone'],
                order_data['telegram_username'],
                order_data['source'],
                order_data['created_at'],
                order_data['created_at']
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving order to database: {e}")

# Integration functions for the main bot

async def start_telegram_parser(api_id: str, api_hash: str, phone: str):
    """Start the Telegram group parser in background"""
    parser = TelegramGroupParser(api_id, api_hash, phone)
    await parser.start_monitoring()

def setup_telegram_parser_task(api_id: str, api_hash: str, phone: str):
    """Setup background task for Telegram parsing"""
    loop = asyncio.get_event_loop()
    task = loop.create_task(start_telegram_parser(api_id, api_hash, phone))
    return task
