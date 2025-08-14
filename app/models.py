"""
Database models for the Yukuz Logistics Bot
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, Enum as SQLEnum, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class AnnouncementType(str, Enum):
    """Announcement type enumeration"""
    CARGO = "cargo"
    TRANSPORT = "transport"


class AnnouncementStatus(str, Enum):
    """Announcement status enumeration"""
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
    REJECTED = "rejected"
    EXPIRED = "expired"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    language: Mapped[str] = mapped_column(String(10), default="uz")
    subscription_until: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    free_views_used: Mapped[int] = mapped_column(Integer, default=0)  # Track free detailed views used
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"


class Announcement(Base):
    """Announcement model for cargo and transport"""
    __tablename__ = "announcements"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    type: Mapped[AnnouncementType] = mapped_column(SQLEnum(AnnouncementType), nullable=False)
    status: Mapped[AnnouncementStatus] = mapped_column(SQLEnum(AnnouncementStatus), default=AnnouncementStatus.DRAFT)
    
    # Common fields
    from_location: Mapped[str] = mapped_column(String(255), nullable=False)
    to_location: Mapped[str] = mapped_column(String(255), nullable=False)
    departure_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    contact_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    contact_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Cargo specific fields
    cargo_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    cargo_weight: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    cargo_volume: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Transport specific fields
    transport_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    transport_capacity: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    transport_model: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # System fields
    message_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    channel_message_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    moderated_by: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    moderated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Announcement(id={self.id}, type={self.type}, status={self.status})>"
    
    @property
    def is_cargo(self) -> bool:
        """Check if announcement is cargo type"""
        return self.type == AnnouncementType.CARGO
    
    @property
    def is_transport(self) -> bool:
        """Check if announcement is transport type"""
        return self.type == AnnouncementType.TRANSPORT
    
    def get_display_text(self, language: str = "uz") -> str:
        """Get formatted display text for the announcement"""
        if language == "ru":
            return self._get_russian_text()
        return self._get_uzbek_text()
    
    def _get_uzbek_text(self) -> str:
        """Get Uzbek formatted text"""
        if self.is_cargo:
            return self._format_cargo_uzbek()
        return self._format_transport_uzbek()
    
    def _get_russian_text(self) -> str:
        """Get Russian formatted text"""
        if self.is_cargo:
            return self._format_cargo_russian()
        return self._format_transport_russian()
    
    def _format_cargo_uzbek(self) -> str:
        """Format cargo announcement in Uzbek"""
        text = f"📦 <b>ЮК ЭЪЛОНИ</b>\n\n"
        text += f"📍 <b>Дан:</b> {self.from_location}\n"
        text += f"📍 <b>Гача:</b> {self.to_location}\n"
        
        if self.cargo_type:
            text += f"📋 <b>Юк тури:</b> {self.cargo_type}\n"
        if self.cargo_weight:
            text += f"⚖️ <b>Оғирлиги:</b> {self.cargo_weight}\n"
        if self.cargo_volume:
            text += f"📏 <b>Ҳажми:</b> {self.cargo_volume}\n"
        if self.departure_date:
            text += f"📅 <b>Чиқиш санаси:</b> {self.departure_date}\n"
        if self.price:
            text += f"💰 <b>Нархи:</b> {self.price}\n"
        if self.description:
            text += f"📝 <b>Қўшимча маълумот:</b> {self.description}\n"
        
        text += f"\n📞 <b>Алоқа:</b> {self.contact_phone}"
        if self.contact_name:
            text += f" ({self.contact_name})"
        
        return text
    
    def _format_cargo_russian(self) -> str:
        """Format cargo announcement in Russian"""
        text = f"📦 <b>ОБЪЯВЛЕНИЕ О ГРУЗЕ</b>\n\n"
        text += f"📍 <b>Откуда:</b> {self.from_location}\n"
        text += f"📍 <b>Куда:</b> {self.to_location}\n"
        
        if self.cargo_type:
            text += f"📋 <b>Тип груза:</b> {self.cargo_type}\n"
        if self.cargo_weight:
            text += f"⚖️ <b>Вес:</b> {self.cargo_weight}\n"
        if self.cargo_volume:
            text += f"📏 <b>Объем:</b> {self.cargo_volume}\n"
        if self.departure_date:
            text += f"📅 <b>Дата отправления:</b> {self.departure_date}\n"
        if self.price:
            text += f"💰 <b>Цена:</b> {self.price}\n"
        if self.description:
            text += f"📝 <b>Дополнительно:</b> {self.description}\n"
        
        text += f"\n📞 <b>Контакт:</b> {self.contact_phone}"
        if self.contact_name:
            text += f" ({self.contact_name})"
        
        return text
    
    def _format_transport_uzbek(self) -> str:
        """Format transport announcement in Uzbek"""
        text = f"🚛 <b>ТРАНСПОРТ ЭЪЛОНИ</b>\n\n"
        text += f"📍 <b>Дан:</b> {self.from_location}\n"
        text += f"📍 <b>Гача:</b> {self.to_location}\n"
        
        if self.transport_type:
            text += f"🚚 <b>Транспорт тури:</b> {self.transport_type}\n"
        if self.transport_model:
            text += f"🏷️ <b>Модели:</b> {self.transport_model}\n"
        if self.transport_capacity:
            text += f"📦 <b>Сиғими:</b> {self.transport_capacity}\n"
        if self.departure_date:
            text += f"📅 <b>Чиқиш санаси:</b> {self.departure_date}\n"
        if self.price:
            text += f"💰 <b>Нархи:</b> {self.price}\n"
        if self.description:
            text += f"📝 <b>Қўшимча маълумот:</b> {self.description}\n"
        
        text += f"\n📞 <b>Алоқа:</b> {self.contact_phone}"
        if self.contact_name:
            text += f" ({self.contact_name})"
        
        return text
    
    def _format_transport_russian(self) -> str:
        """Format transport announcement in Russian"""
        text = f"🚛 <b>ОБЪЯВЛЕНИЕ О ТРАНСПОРТЕ</b>\n\n"
        text += f"📍 <b>Откуда:</b> {self.from_location}\n"
        text += f"📍 <b>Куда:</b> {self.to_location}\n"
        
        if self.transport_type:
            text += f"🚚 <b>Тип транспорта:</b> {self.transport_type}\n"
        if self.transport_model:
            text += f"🏷️ <b>Модель:</b> {self.transport_model}\n"
        if self.transport_capacity:
            text += f"📦 <b>Вместимость:</b> {self.transport_capacity}\n"
        if self.departure_date:
            text += f"📅 <b>Дата отправления:</b> {self.departure_date}\n"
        if self.price:
            text += f"💰 <b>Цена:</b> {self.price}\n"
        if self.description:
            text += f"📝 <b>Дополнительно:</b> {self.description}\n"
        
        text += f"\n📞 <b>Контакт:</b> {self.contact_phone}"
        if self.contact_name:
            text += f" ({self.contact_name})"
        
        return text
