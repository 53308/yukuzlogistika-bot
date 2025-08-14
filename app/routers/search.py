"""
Detail view router for cargo and transport listings with contact access control
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
    """Check if user can access contact information (subscription OR free views available OR system owners)"""
    # System owners always have full access
    if user.id in [8101326669, 6484968606]:  # @b1snesf and second owner
        return True
        
    # Check if user has active subscription
    if (hasattr(user, 'subscription_until') and 
        user.subscription_until is not None and 
        user.subscription_until > datetime.now()):
        return True
    
    # Check if user has free contact accesses remaining (first 5 are free)
    free_views_used = getattr(user, 'free_views_used', 0)
    free_views_remaining = 5 - free_views_used
    return free_views_remaining > 0

def is_system_owner(user: User) -> bool:
    """Check if user is system owner with unlimited access"""
    return user.id in [8101326669, 6484968606]

def get_free_views_remaining(user: User) -> int:
    """Get number of free detailed views remaining for user"""
    free_views_used = getattr(user, 'free_views_used', 0)
    return max(0, 5 - free_views_used)

def get_access_status_text(user: User, language: str) -> str:
    """Get access status text based on user's subscription and free views"""
    # System owners get special status
    if is_system_owner(user):
        if language == "ru":
            return "👑 Безлимитный доступ (владелец системы)"
        elif language == "uz_cyrillic": 
            return "👑 Чексiz кириш (тизим эгаси)"
        else:
            return "👑 Cheksiz kirish (tizim egasi)"
    
    has_subscription = (hasattr(user, 'subscription_until') and 
                       user.subscription_until is not None and 
                       user.subscription_until > datetime.now())
    
    if has_subscription:
        if language == "ru":
            return "✅ У вас активная подписка"
        elif language == "uz_cyrillic": 
            return "✅ Сизда фаол обуна бор"
        else:
            return "✅ Sizda faol obuna bor"
    
    free_remaining = get_free_views_remaining(user)
    if free_remaining > 0:
        if language == "ru":
            return f"🆓 Бесплатных обращений к контактам: {free_remaining}/5"
        elif language == "uz_cyrillic":
            return f"🆓 Бепул контакт мурожаатлари: {free_remaining}/5"
        else:
            return f"🆓 Bepul kontakt murojaat: {free_remaining}/5"
    
    if language == "ru":
        return "🔒 Нужна подписка для доступа к контактам"
    elif language == "uz_cyrillic":
        return "🔒 Контактларга кириш учун обуна керак"
    else:
        return "🔒 Kontaktlarga kirish uchun obuna kerak"


async def format_detailed_cargo_view_with_access(listing, can_access: bool, user: User, language: str) -> tuple[str, InlineKeyboardMarkup]:
    """Format detailed cargo listing view"""
    
    # Header with route
    text = f"<b>{listing.origin} → {listing.destination}</b>\n\n"
    
    # Cargo details
    if hasattr(listing, 'description') and listing.description:
        desc = listing.description[:200] if len(listing.description) > 200 else listing.description
        text += f"📦 <b>Yuk:</b> {desc}\n\n"
    
    # Transport type
    text += f"🚚 <b>Transport:</b> {listing.cargo_type}\n"
    
    # Weight
    if listing.weight:
        text += f"⚖️ <b>Vazn:</b> {listing.weight}\n"
    
    # Route details (mock for consistency with reference bot)
    text += f"🛣️ <b>Masofa:</b> 345 km\n"
    text += f"⏱️ <b>Vaqt:</b> 6.1 soat\n\n"
    
    # Price if available
    if listing.price:
        text += f"💰 <b>Narx:</b> {listing.price}\n\n"
    
    # Loading date
    text += f"📅 <b>Yuklash sanasi:</b> {listing.date_posted.strftime('%d %B')}\n\n"
    
    # Contact section
    text += "📞 <b>Aloqa:</b>\n"
    
    # Create keyboard based on subscription status
    keyboard = InlineKeyboardBuilder()
    
    # Check if user can access contacts (subscription OR free views)
    can_access = can_access_contacts(user)
    
    # Always show access status 
    access_status = get_access_status_text(user, language)
    text += f"\n{access_status}\n\n"
    
    if can_access:
        # User can access contacts - show contact options
        keyboard.add(InlineKeyboardButton(
            text="💬 Перейти к сообщению",
            callback_data=f"message_{listing.id}"
        ))
        
        if listing.contact:
            keyboard.add(InlineKeyboardButton(
                text="📞 Номер телефона",
                callback_data=f"phone_{listing.id}"
            ))
    else:
        # No contact access - show subscription offer
        if language == "ru":
            text += "🔒 Для доступа к контактам нужна подписка\n"
            text += "🆓 У вас было 5 бесплатных обращений к контактам\n"
        elif language == "uz_cyrillic":
            text += "🔒 Контактларга кириш учун обуна керак\n"
            text += "🆓 Сизда 5 та бепул контакт мурожаати бор эди\n"
        else:
            text += "🔒 Kontaktlarga kirish uchun obuna kerak\n"
            text += "🆓 Sizda 5 ta bepul kontakt murojaat bor edi\n"
        
        # Auto-suggest subscription
        keyboard.add(InlineKeyboardButton(
            text="💳 Купить подписку" if language == "ru" else "💳 Obuna sotib olish",
            callback_data="show_subscriptions"
        ))
    
    keyboard.add(InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="back_to_search"
    ))
    
    return text, keyboard.as_markup()


@router.callback_query(F.data.startswith("detail_"))
async def show_detailed_view(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User,
    language: str
):
    """Show detailed view of cargo/transport listing with free views tracking"""
    try:
        if not callback.data:
            await callback.answer("❌ Ошибка данных", show_alert=True)
            return
        listing_id = callback.data.split("_")[1]
        
        # Get listing from data service
        cargo_listings = await data_service.get_cargo_listings()
        listing = None
        
        for cargo in cargo_listings:
            if cargo.id == listing_id:
                listing = cargo
                break
        
        if not listing:
            await callback.answer("❌ Э'лон топилмади", show_alert=True)
            return
        
        # Always show detailed order information (no restrictions on viewing order details)
        # Contact access restrictions only apply to phone/message buttons
        can_access = can_access_contacts(user)
        
        # Format detailed view with new access logic
        text, keyboard = await format_detailed_cargo_view_with_access(listing, can_access, user, language)
        
        if callback.message and hasattr(callback.message, 'edit_text'):
            await callback.message.edit_text(
                text,
                parse_mode="HTML", 
                reply_markup=keyboard
            )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error showing detail view: {e}")
        await callback.answer("❌ Хатолик юз берди", show_alert=True)


@router.callback_query(F.data.startswith("phone_"))
async def show_phone_number(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User
):
    """Show phone number if user has contact access"""
    try:
        if not callback.data:
            await callback.answer("❌ Ошибка данных", show_alert=True)
            return
        listing_id = callback.data.split("_")[1]
        
        # Check if user can access contacts
        can_access = can_access_contacts(user)
        
        if not can_access:
            await callback.answer("🔒 Для доступа к контактам нужна подписка", show_alert=True)
            return
            
        # If user is not system owner and not subscriber, count this as contact access
        if not is_system_owner(user):
            has_subscription = (hasattr(user, 'subscription_until') and 
                               user.subscription_until is not None and 
                               user.subscription_until > datetime.now())
            
            if not has_subscription:
                # User is using a free contact access - increment counter
                current_free_views = getattr(user, 'free_views_used', 0)
                
                # Update free views in database using raw SQL
                from sqlalchemy import text
                await session.execute(
                    text("UPDATE users SET free_views_used = :views WHERE id = :user_id"),
                    {"views": current_free_views + 1, "user_id": user.id}
                )
                await session.commit()
                
                # Update user object for current session
                user.free_views_used = current_free_views + 1
        
        # Get listing
        cargo_listings = await data_service.get_cargo_listings()
        listing = None
        
        for cargo in cargo_listings:
            if cargo.id == listing_id:
                listing = cargo
                break
        
        if listing and listing.contact:
            await callback.answer(f"📞 {listing.contact}", show_alert=True)
        else:
            await callback.answer("📞 Telefon raqam mavjud emas", show_alert=True)
            
    except Exception as e:
        logger.error(f"Error showing phone: {e}")
        await callback.answer("❌ Хатолик", show_alert=True)


@router.callback_query(F.data.startswith("message_"))
async def redirect_to_sender(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User
):
    """Redirect to message sender (contact access required)"""
    try:
        if not callback.data:
            await callback.answer("❌ Ошибка данных", show_alert=True)
            return
        listing_id = callback.data.split("_")[1]
        
        # Check if user can access contacts
        can_access = can_access_contacts(user)
        
        if not can_access:
            await callback.answer("🔒 Для доступа к контактам нужна подписка", show_alert=True)
            return
            
        # If user is not system owner and not subscriber, count this as contact access
        if not is_system_owner(user):
            has_subscription = (hasattr(user, 'subscription_until') and 
                               user.subscription_until is not None and 
                               user.subscription_until > datetime.now())
            
            if not has_subscription:
                # User is using a free contact access - increment counter
                current_free_views = getattr(user, 'free_views_used', 0)
                
                # Update free views in database using raw SQL
                from sqlalchemy import text
                await session.execute(
                    text("UPDATE users SET free_views_used = :views WHERE id = :user_id"),
                    {"views": current_free_views + 1, "user_id": user.id}
                )
                await session.commit()
                
                # Update user object for current session
                user.free_views_used = current_free_views + 1
        
        # Get listing
        cargo_listings = await data_service.get_cargo_listings()
        listing = None
        
        for cargo in cargo_listings:
            if cargo.id == listing_id:
                listing = cargo
                break
        
        if listing:
            # Create direct link to sender (mock username for demo)
            sender_username = "logistics_sender"  # In real implementation, extract from source
            direct_link = f"https://t.me/{sender_username}"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💬 Перейти к отправителю", url=direct_link)],
                [InlineKeyboardButton(text="🔙 Назад", callback_data=f"detail_{listing_id}")]
            ])
            
            text = (
                f"💬 <b>Связаться с отправителем</b>\n\n"
                f"Нажмите кнопку ниже для перехода к отправителю сообщения.\n"
                f"Доступно только подписчикам и пользователям с бесплатными обращениями."
            )
            
            if callback.message and hasattr(callback.message, 'edit_text'):
                await callback.message.edit_text(
                    text,
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
        else:
            await callback.answer("❌ Объявление не найдено", show_alert=True)
            
    except Exception as e:
        logger.error(f"Error redirecting to sender: {e}")
        await callback.answer("❌ Хатолик", show_alert=True)


@router.callback_query(F.data == "back_to_search")
async def back_to_search(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User,
    language: str
):
    """Return to search results"""
    try:
        # Get fresh listings
        cargo_listings = await data_service.get_cargo_listings(limit=5)
        
        text = f"🚚 Tent uchun {len(cargo_listings)} ta e'lon topildi"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")]
        ])
        
        if callback.message:
            await callback.message.edit_text(text, reply_markup=keyboard)
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error returning to search: {e}")
        await callback.answer("❌ Хатолик", show_alert=True)
