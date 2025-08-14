"""
Detail view router for cargo and transport listings
"""

import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.models import User
from app.services.data_service import data_service

logger = logging.getLogger(__name__)

router = Router()


def can_access_contacts(user: User) -> bool:
    """Check if user can access contact information"""
    # System owners always have full access
    if user.id in [8101326669, 6484968606]:
        return True
        
    # Check if user has active subscription
    if (hasattr(user, 'subscription_until') and 
        user.subscription_until is not None and 
        user.subscription_until > datetime.now()):
        return True
    
    # Check if user has free contact accesses remaining
    free_views_used = getattr(user, 'free_views_used', 0)
    return (5 - free_views_used) > 0


@router.callback_query(F.data.startswith("detail_"))
async def show_detailed_view(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User,
    language: str
):
    """Show detailed view of cargo/transport listing"""
    try:
        listing_id = callback.data.split("_")[1]
        
        # Get listing from data service
        cargo_listings = await data_service.get_cargo_listings()
        listing = None
        
        for cargo in cargo_listings:
            if cargo.id == listing_id:
                listing = cargo
                break
        
        if not listing:
            await callback.answer("❌ Объявление не найдено", show_alert=True)
            return
        
        # Format detailed view
        text = f"<b>{listing.origin} → {listing.destination}</b>\n\n"
        
        if hasattr(listing, 'description') and listing.description:
            text += f"📦 <b>Груз:</b> {listing.description}\n\n"
        
        text += f"🚚 <b>Транспорт:</b> {listing.cargo_type}\n"
        
        if listing.weight:
            text += f"⚖️ <b>Вес:</b> {listing.weight}\n"
        
        if listing.price:
            text += f"💰 <b>Цена:</b> {listing.price}\n\n"
        
        text += f"📅 <b>Дата:</b> {listing.date_posted.strftime('%d %B')}\n\n"
        
        # Create keyboard
        keyboard = InlineKeyboardBuilder()
        
        # Check contact access
        can_access = can_access_contacts(user)
        
        if can_access:
            keyboard.add(InlineKeyboardButton(
                text="💬 Связаться",
                callback_data=f"contact_{listing.id}"
            ))
            
            if listing.contact:
                keyboard.add(InlineKeyboardButton(
                    text="📞 Телефон",
                    callback_data=f"phone_{listing.id}"
                ))
        else:
            text += "🔒 Для доступа к контактам нужна подписка\n"
            keyboard.add(InlineKeyboardButton(
                text="💳 Купить подписку",
                callback_data="buy_subscription"
            ))
        
        keyboard.add(InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="back_to_search"
        ))
        
        if callback.message:
            await callback.message.edit_text(
                text,
                parse_mode="HTML",
                reply_markup=keyboard.as_markup()
            )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error showing detail view: {e}")
        await callback.answer("❌ Ошибка", show_alert=True)


@router.callback_query(F.data.startswith("phone_"))
async def show_phone_number(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User
):
    """Show phone number if user has access"""
    try:
        listing_id = callback.data.split("_")[1]
        
        if not can_access_contacts(user):
            await callback.answer("🔒 Нужна подписка", show_alert=True)
            return
        
        # Update free views counter if not system owner/subscriber
        if user.id not in [8101326669, 6484968606]:
            has_subscription = (hasattr(user, 'subscription_until') and 
                               user.subscription_until is not None and 
                               user.subscription_until > datetime.now())
            
            if not has_subscription:
                current_free_views = getattr(user, 'free_views_used', 0)
                await session.execute(
                    text("UPDATE users SET free_views_used = :views WHERE id = :user_id"),
                    {"views": current_free_views + 1, "user_id": user.id}
                )
                await session.commit()
                user.free_views_used = current_free_views + 1
        
        # Get listing and show phone
        cargo_listings = await data_service.get_cargo_listings()
        listing = None
        
        for cargo in cargo_listings:
            if cargo.id == listing_id:
                listing = cargo
                break
        
        if listing and listing.contact:
            await callback.answer(f"📞 {listing.contact}", show_alert=True)
        else:
            await callback.answer("📞 Номер недоступен", show_alert=True)
            
    except Exception as e:
        logger.error(f"Error showing phone: {e}")
        await callback.answer("❌ Ошибка", show_alert=True)
