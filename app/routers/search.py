"""Search functionality"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.keyboards import get_cargo_transport_choice, get_vehicle_types_keyboard
from app.models import get_db_connection
import logging
import math
import random
from datetime import datetime

router = Router()
logger = logging.getLogger(__name__)

class SearchState(StatesGroup):
    waiting_search_type = State()
    waiting_country_choice = State()
    waiting_city_choice = State()
    waiting_vehicle_choice = State()
    waiting_city_input = State()

# Extended city database with coordinates from Uzbekistan logistics bot data
CITY_COORDINATES = {
    # Major cities of Uzbekistan
    'ташкент': (41.2995, 69.2401),
    'tashkent': (41.2995, 69.2401),
    'toshkent': (41.2995, 69.2401),
    'самарканд': (39.6270, 66.9750),
    'samarkand': (39.6270, 66.9750),
    'samarqand': (39.6270, 66.9750),
    'наманган': (40.9983, 71.6726),
    'namangan': (40.9983, 71.6726),
    'андижан': (40.7821, 72.3442),
    'andijon': (40.7821, 72.3442),
    'andijan': (40.7821, 72.3442),
    'фергана': (40.3734, 71.7978),
    'fargona': (40.3734, 71.7978),
    'fergana': (40.3734, 71.7978),
    'бухара': (39.7747, 64.4286),
    'buxoro': (39.7747, 64.4286),
    'bukhara': (39.7747, 64.4286),
    'хива': (41.3775, 60.3619),
    'xiva': (41.3775, 60.3619),
    'khiva': (41.3775, 60.3619),
    'нукус': (42.4731, 59.6103),
    'nukus': (42.4731, 59.6103),
    'qarshi': (38.8606, 65.7890),
    'карши': (38.8606, 65.7890),
    'кокан': (40.5272, 70.9409),
    'qoqon': (40.5272, 70.9409),
    'kokand': (40.5272, 70.9409),
    'термез': (37.2242, 67.2783),
    'termiz': (37.2242, 67.2783),
    'termez': (37.2242, 67.2783),
    'жиззах': (40.1158, 67.8420),
    'jizzax': (40.1158, 67.8420),
    'jizzakh': (40.1158, 67.8420),
    'навои': (40.0844, 65.3792),
    'navoiy': (40.0844, 65.3792),
    'navoi': (40.0844, 65.3792),
    'гулистан': (40.4897, 68.7842),
    'guliston': (40.4897, 68.7842),
    'gulistan': (40.4897, 68.7842),
    'ургенч': (41.5500, 60.6333),
    'urganch': (41.5500, 60.6333),
    'urgench': (41.5500, 60.6333),
    
    # Tashkent region cities
    'ангрен': (41.0167, 70.1436),
    'angren': (41.0167, 70.1436),
    'алмалык': (40.8547, 69.5997),
    'olmaliq': (40.8547, 69.5997),
    'almalyk': (40.8547, 69.5997),
    'бекабад': (40.2139, 69.2661),
    'bekobod': (40.2139, 69.2661),
    'bekabad': (40.2139, 69.2661),
    'янгиюль': (41.1122, 69.0428),
    'yangiyul': (41.1122, 69.0428),
    'чирчик': (41.4669, 69.5831),
    'chirchiq': (41.4669, 69.5831),
    'chirchik': (41.4669, 69.5831),
    'газалкент': (41.5333, 69.2167),
    'gazalkent': (41.5333, 69.2167),
    'пскент': (41.0333, 68.9000),
    'pskent': (41.0333, 68.9000),
    'чиназ': (40.9383, 68.7989),
    'chinoz': (40.9383, 68.7989),
    'chinaz': (40.9383, 68.7989),
    
    # International cities
    'москва': (55.7558, 37.6176),
    'moscow': (55.7558, 37.6176),
    'алматы': (43.2220, 76.8512),
    'almaty': (43.2220, 76.8512),
    'olmata': (43.2220, 76.8512),
    'стамбул': (41.0082, 28.9784),
    'istanbul': (41.0082, 28.9784),
    'грозный': (43.3183, 45.6906),
    'grozny': (43.3183, 45.6906),
    'астана': (51.1694, 71.4491),
    'nur-sultan': (51.1694, 71.4491),
    'астрахань': (46.3497, 48.0408),
    'astrakhan': (46.3497, 48.0408),
    'волгоград': (48.7080, 44.5133),
    'volgograd': (48.7080, 44.5133),
    'краснодар': (45.0401, 38.9758),
    'krasnodar': (45.0401, 38.9758),
    'ростов': (47.2357, 39.7015),
    'rostov': (47.2357, 39.7015),
    'новосибирск': (55.0084, 82.9357),
    'novosibirsk': (55.0084, 82.9357),
    'екатеринбург': (56.8431, 60.6454),
    'ekaterinburg': (56.8431, 60.6454),
    'казань': (55.8304, 49.0661),
    'kazan': (55.8304, 49.0661),
    'уфа': (54.7388, 55.9721),
    'ufa': (54.7388, 55.9721),
    'челябинск': (55.1644, 61.4368),
    'chelyabinsk': (55.1644, 61.4368),
    'омск': (54.9885, 73.3242),
    'omsk': (54.9885, 73.3242),
    'пермь': (58.0105, 56.2502),
    'perm': (58.0105, 56.2502)
}

def calculate_distance_and_time(city1: str, city2: str):
    """Calculate distance and travel time between cities"""
    city1_lower = city1.lower().strip()
    city2_lower = city2.lower().strip()
    
    coords1 = CITY_COORDINATES.get(city1_lower)
    coords2 = CITY_COORDINATES.get(city2_lower)
    
    if not coords1 or not coords2:
        return 0, 0.0
    
    # Haversine formula
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1 = math.radians(coords1[0]), math.radians(coords1[1])
    lat2, lon2 = math.radians(coords2[0]), math.radians(coords2[1])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    distance = int(R * c)
    travel_time = distance / 65  # 65 km/h average speed
    
    return distance, travel_time

def get_country_flag(city: str) -> str:
    """Get country flag emoji for city - expanded database"""
    city_lower = city.lower().strip()
    
    # Uzbekistan cities (expanded list from logistics bot data)
    uz_cities = [
        # Major cities
        'ташкент', 'tashkent', 'toshkent', 'самарканд', 'samarkand', 'samarqand',
        'наманган', 'namangan', 'андижан', 'andijon', 'andijan', 'фергана', 'fargona', 'fergana',
        'бухара', 'buxoro', 'bukhara', 'хива', 'xiva', 'khiva', 'нукус', 'nukus',
        'карши', 'qarshi', 'кокан', 'qoqon', 'kokand', 'термез', 'termiz', 'termez',
        'жиззах', 'jizzax', 'jizzakh', 'навои', 'navoiy', 'navoi', 'гулистан', 'guliston', 'gulistan',
        'ургенч', 'urganch', 'urgench',
        # Tashkent region
        'ангрен', 'angren', 'алмалык', 'olmaliq', 'almalyk', 'бекабад', 'bekobod', 'bekabad',
        'янгиюль', 'yangiyul', 'чирчик', 'chirchiq', 'chirchik', 'газалкент', 'gazalkent',
        'пскент', 'pskent', 'чиназ', 'chinoz', 'chinaz', 'хорзига', 'xorazm'
    ]
    
    # Russian cities (expanded)
    ru_cities = [
        'москва', 'moscow', 'грозный', 'grozny', 'астрахань', 'astrakhan',
        'волгоград', 'volgograd', 'краснодар', 'krasnodar', 'ростов', 'rostov',
        'новосибирск', 'novosibirsk', 'екатеринбург', 'ekaterinburg',
        'казань', 'kazan', 'уфа', 'ufa', 'челябинск', 'chelyabinsk',
        'омск', 'omsk', 'пермь', 'perm', 'санкт-петербург', 'saint-petersburg',
        'нижний новгород', 'nizhny novgorod'
    ]
    
    # Kazakhstan cities
    kz_cities = ['алматы', 'almaty', 'olmata', 'астана', 'nur-sultan', 'шымкент', 'shymkent']
    
    # Turkey cities
    tr_cities = ['стамбул', 'istanbul', 'анкара', 'ankara', 'измир', 'izmir']
    
    if city_lower in uz_cities:
        return '🇺🇿'
    elif city_lower in ru_cities:
        return '🇷🇺'
    elif city_lower in kz_cities:
        return '🇰🇿'  
    elif city_lower in tr_cities:
        return '🇹🇷'
    else:
        return '🌍'

def format_time_ago(created_at) -> str:
    """Format time ago text exactly like original - shows '4 минуты назад' etc"""
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
    
    import pytz
    now = datetime.now(pytz.UTC)
    
    if created_at.tzinfo is None:
        created_at = pytz.utc.localize(created_at)
    
    diff = now - created_at
    total_seconds = int(diff.total_seconds())
    
    if diff.days > 7:
        return f"{diff.days} дней назад"
    elif diff.days > 0:
        if diff.days == 1:
            return "1 день назад"
        elif diff.days in [2, 3, 4]:
            return f"{diff.days} дня назад"
        else:
            return f"{diff.days} дней назад"
    elif total_seconds >= 3600:
        hours = total_seconds // 3600
        if hours == 1:
            return "1 час назад"
        elif hours in [2, 3, 4]:
            return f"{hours} часа назад"
        else:
            return f"{hours} часов назад"
    else:
        minutes = max(1, total_seconds // 60)
        if minutes == 1:
            return "1 минуту назад"
        elif minutes in [2, 3, 4]:
            return f"{minutes} минуты назад"
        else:
            return f"{minutes} минут назад"

@router.message(F.text == "🔍 Быстрый Поиск")
async def quick_search_handler(message: Message, state: FSMContext):
    """Quick search handler - shows search type selection like original with bottom keyboard"""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    
    text = "Выберите нужный раздел поиска"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Найти груз")],
            [KeyboardButton(text="🚛 Найти транспорт")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer(text, reply_markup=keyboard)
    await state.set_state(SearchState.waiting_search_type)

@router.message(F.text == "📦 Найти груз")
async def find_cargo_from_search(message: Message, state: FSMContext):
    """Find cargo from search menu - show country selection"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    countries_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 Узбекистан - 503", callback_data="country_uz_cargo"),
            InlineKeyboardButton(text="🇦🇫 Афганистан - 2", callback_data="country_af_cargo")
        ],
        [
            InlineKeyboardButton(text="🇧🇾 Белоруссия - 7", callback_data="country_by_cargo"),
            InlineKeyboardButton(text="🇭🇺 Венгрия - 1", callback_data="country_hu_cargo")
        ],
        [
            InlineKeyboardButton(text="🇩🇪 Германия - 2", callback_data="country_de_cargo"),
            InlineKeyboardButton(text="🇬🇪 Грузия - 1", callback_data="country_ge_cargo")
        ],
        [
            InlineKeyboardButton(text="🇰🇿 Казахстан - 7", callback_data="country_kz_cargo"),
            InlineKeyboardButton(text="🇰🇬 Каракалпакстан - 6", callback_data="country_kk_cargo")
        ],
        [
            InlineKeyboardButton(text="🇰🇬 Кыргызстан - 1", callback_data="country_kg_cargo"),
            InlineKeyboardButton(text="🇷🇺 Россия - 25", callback_data="country_ru_cargo")
        ],
        [
            InlineKeyboardButton(text="🇹🇯 Таджикистан - 2", callback_data="country_tj_cargo"),
            InlineKeyboardButton(text="🇹🇲 Туркменистан - 1", callback_data="country_tm_cargo")
        ],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_search_menu")]
    ])
    
    await message.answer(
        "🔍 <b>Быстрый Поиск</b>\n\n"
        "🚚 Выберите нужный раздел поиска\n\n"
        "📦 <b>Найти груз</b>\n"
        "🚚⚡⚡⚡⚡ 12:58\n\n"
        "📦 <b>Найдено 599 объявлений, 107 из них сегодня</b>",
        reply_markup=countries_keyboard,
        parse_mode="HTML"
    )
    await state.set_state(SearchState.waiting_country_choice)
    await state.update_data(search_type="cargo")

@router.message(F.text == "🚛 Найти транспорт")
async def find_transport_from_search(message: Message, state: FSMContext):
    """Find transport from search menu - show country selection"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    countries_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 Узбекистан - 503", callback_data="country_uz_transport"),
            InlineKeyboardButton(text="🇦🇫 Афганистан - 2", callback_data="country_af_transport")
        ],
        [
            InlineKeyboardButton(text="🇧🇾 Белоруссия - 7", callback_data="country_by_transport"),
            InlineKeyboardButton(text="🇭🇺 Венгрия - 1", callback_data="country_hu_transport")
        ],
        [
            InlineKeyboardButton(text="🇩🇪 Германия - 2", callback_data="country_de_transport"),
            InlineKeyboardButton(text="🇬🇪 Грузия - 1", callback_data="country_ge_transport")
        ],
        [
            InlineKeyboardButton(text="🇰🇿 Казахстан - 7", callback_data="country_kz_transport"),
            InlineKeyboardButton(text="🇰🇬 Каракалпакстан - 6", callback_data="country_kk_transport")
        ],
        [
            InlineKeyboardButton(text="🇰🇬 Кыргызстан - 1", callback_data="country_kg_transport"),
            InlineKeyboardButton(text="🇷🇺 Россия - 25", callback_data="country_ru_transport")
        ],
        [
            InlineKeyboardButton(text="🇹🇯 Таджикистан - 2", callback_data="country_tj_transport"),
            InlineKeyboardButton(text="🇹🇲 Туркменистан - 1", callback_data="country_tm_transport")
        ],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_search_menu")]
    ])
    
    await message.answer(
        "🔍 <b>Быстрый Поиск</b>\n\n"
        "🚚 Выберите нужный раздел поиска\n\n"
        "🚚 <b>Найти транспорт</b>\n"
        "🚚⚡⚡⚡⚡ 12:58\n\n"
        "🚚 <b>Найдено 498 объявлений, 91 из них сегодня</b>",
        reply_markup=countries_keyboard,
        parse_mode="HTML"
    )
    await state.set_state(SearchState.waiting_country_choice)
    await state.update_data(search_type="transport")

# Country selection callback handlers  
@router.callback_query(F.data.startswith("country_"))
async def handle_country_callback(callback_query: CallbackQuery, state: FSMContext):
    """Handle country selection callbacks"""
    from app.country_handlers import handle_country_selection
    await handle_country_selection(callback_query, state)

# City selection callback handlers
@router.callback_query(F.data.startswith("city_"))
async def handle_city_callback(callback_query: CallbackQuery, state: FSMContext):
    """Handle city selection callbacks"""
    from app.country_handlers import handle_city_selection
    await handle_city_selection(callback_query, state)

# Search function for cities
async def perform_search_by_city(callback_query: CallbackQuery, city_name: str, search_type: str, state: FSMContext):
    """Perform search by city name"""
    try:
        # Import comprehensive city database
        from app.city_database import get_city_variants
        
        # Get ALL possible variants for the city
        search_variants = get_city_variants(city_name.lower())
        
        import psycopg2
        import os
        
        # Connect to PostgreSQL database
        DATABASE_URL = os.getenv('DATABASE_URL')
        if not DATABASE_URL:
            await callback_query.message.answer("❌ Ошибка подключения к базе данных")
            return
            
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Build query based on search type
        if search_type == "cargo":
            query = "SELECT * FROM announcements WHERE announcement_type = 'cargo'"
        else:
            query = "SELECT * FROM announcements WHERE announcement_type = 'transport'"
        
        # Add city search conditions
        conditions = []
        city_conditions = []
        for variant in search_variants:
            city_conditions.append(f"LOWER(from_location) LIKE '%{variant.lower()}%' OR LOWER(to_location) LIKE '%{variant.lower()}%'")
        
        if city_conditions:
            conditions.append(f"({' OR '.join(city_conditions)})")
        
        if conditions:
            query += " AND " + " AND ".join(conditions)
        
        query += " ORDER BY created_at DESC LIMIT 6"
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not results:
            await callback_query.message.edit_text(f"❌ По запросу '{city_name}' ничего не найдено.")
            return
        
        # Send results as individual messages exactly like original
        search_icon = "📦" if search_type == "cargo" else "🚚"
        await callback_query.message.edit_text(f"🔍 Результаты поиска {search_icon} в {city_name}:")
        
        for i, row in enumerate(results[:5], 1):
            # Unpack all columns from database
            (announcement_id, title, description, ann_type, status, from_loc, to_loc, 
             cargo_type, vehicle_type, weight_capacity, contact_name, contact_phone, 
             telegram_username, price_per_ton, departure_date, estimated_delivery, 
             special_requirements, source, user_id, created_at, updated_at) = row
            
            # Get country flag for location
            flag = get_country_flag(from_loc)
            
            # Format time exactly like original
            time_str = format_time_ago(created_at)
            
            # Create message text exactly like original bot
            message_text = f"{i}. {flag} <b>{from_loc} - {to_loc}</b>\n"
            if cargo_type and cargo_type.strip():
                message_text += f"📦 {cargo_type}\n"
            if vehicle_type and vehicle_type.strip():
                message_text += f"🚛 {vehicle_type}\n"
            message_text += f"⏰ {time_str}"
            
            # Create keyboard with "Подробнее" button
            detail_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Подробнее", callback_data=f"detail_{announcement_id}")]
            ])
            
            await callback_query.message.answer(
                message_text, 
                parse_mode="HTML",
                reply_markup=detail_keyboard
            )
        
        # Show "6 из 15 показать больше" button if more results exist
        if len(results) == 6:
            more_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="6 из 15 показать больше", callback_data=f"show_more_{city_name}_{search_type}")]
            ])
            await callback_query.message.answer("", reply_markup=more_keyboard)
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        await callback_query.message.answer(f"❌ Ошибка поиска: {str(e)}")


    await state.set_state(SearchState.waiting_city_input)
    await state.update_data(search_type="transport", vehicle_filter="all")

@router.message(F.text == "🔙 Назад")
async def back_to_main_menu(message: Message, state: FSMContext):
    """Back to main menu"""
    from app.keyboards import get_main_menu
    menu = get_main_menu()
    await message.answer("📦 Бот для поиска грузов и транспорта. Добро пожаловать!", reply_markup=menu)
    await state.clear()

# Menu button handlers with ReplyKeyboardMarkup
@router.message(F.text == "📦 Мои грузы")
async def my_cargo_handler(message: Message):
    """My cargo handler"""
    await message.answer("📦 <b>Мои грузы</b>\n\nУ вас пока нет объявлений о грузах.")

@router.message(F.text == "🚛 Мой транспорт")
async def my_transport_handler(message: Message):
    """My transport handler"""
    await message.answer("🚛 <b>Мой транспорт</b>\n\nУ вас пока нет объявлений о транспорте.")

@router.message(F.text == "📦 Добавить груз")
async def add_cargo_handler(message: Message):
    """Add cargo handler"""
    await message.answer("📦 <b>Добавить груз</b>\n\nОтправьте данные о грузе:\n\n• Откуда\n• Куда\n• Вес\n• Описание\n• Контакт")

@router.message(F.text == "🚛 Добавить транспорт")
async def add_transport_handler(message: Message):
    """Add transport handler"""
    await message.answer("🚛 <b>Добавить транспорт</b>\n\nОтправьте данные о транспорте:\n\n• Тип\n• Откуда\n• Куда\n• Тоннаж\n• Контакт")

@router.message(F.text == "🌐 Изменить язык")
async def change_language_handler(message: Message):
    """Change language handler"""
    await message.answer("🌐 <b>Изменить язык</b>\n\nВыберите язык:\n🇷🇺 Русский\n🇺🇿 O'zbekcha\n🇺🇿 Ўзбекча")

@router.message(F.text == "🔔 Уведомления")
async def notifications_handler(message: Message):
    """Notifications handler"""
    await message.answer("🔔 <b>Уведомления</b>\n\nУведомления включены.")

@router.message(F.text == "💳 Подписка")
async def subscription_handler(message: Message):
    """Subscription handler"""
    await message.answer("💳 <b>Подписка</b>\n\n🆓 Бесплатно: 5 просмотров/день\n💎 Премиум: безлимит за 50,000 сум/месяц")

@router.message(F.text == "📊 Статистика")
async def statistics_handler(message: Message):
    """Statistics handler"""
    await message.answer("📊 <b>Статистика</b>\n\n📦 Объявлений: 5005\n🆕 Новых сегодня: 1604\n👥 Пользователей: 2341")

@router.message(F.text == "📞 Контакты")
async def contacts_handler(message: Message):
    """Contacts handler"""
    await message.answer("📞 <b>Контакты</b>\n\n👨‍💼 Админ: @admin_yuk_uz\n🌐 yukuz.uz\n📧 info@yukuz.uz")

# Callback handlers for menu actions  
@router.callback_query(F.data == "back_main")
async def back_main_callback(callback: CallbackQuery):
    """Back to main menu"""
    if callback.message:
        from app.keyboards import get_main_menu
        menu = get_main_menu()
        await callback.message.answer("📦 Бот для поиска грузов и транспорта. Добро пожаловать!", reply_markup=menu)
    await callback.answer()

@router.callback_query(F.data.startswith("my_"))
async def my_posts_callback(callback: CallbackQuery):
    """My posts handler"""
    if callback.data and callback.message:
        post_type = callback.data.split("_")[1]
        if post_type == "cargo":
            text = "📦 <b>Мои грузы</b>\n\nУ вас пока нет объявлений о грузах."
        else:
            text = "🚛 <b>Мой транспорт</b>\n\nУ вас пока нет объявлений о транспорте."
        await callback.message.edit_text(text)
    await callback.answer()

@router.callback_query(F.data.startswith("add_"))
async def add_post_callback(callback: CallbackQuery):
    """Add post handler"""
    if callback.data and callback.message:
        post_type = callback.data.split("_")[1]
        if post_type == "cargo":
            text = "📦 <b>Добавить груз</b>\n\nОтправьте данные о грузе:\n\n• Откуда\n• Куда\n• Вес\n• Описание\n• Контакт"
        else:
            text = "🚛 <b>Добавить транспорт</b>\n\nОтправьте данные о транспорте:\n\n• Тип\n• Откуда\n• Куда\n• Тоннаж\n• Контакт"
        await callback.message.edit_text(text)
    await callback.answer()

@router.callback_query(F.data.in_(["change_language", "notifications", "subscription", "statistics", "contacts"]))
async def settings_submenu_callback(callback: CallbackQuery):
    """Settings submenu handler"""
    if callback.data and callback.message:
        texts = {
            "change_language": "🌐 <b>Изменить язык</b>\n\nВыберите язык:",
            "notifications": "🔔 <b>Уведомления</b>\n\nУведомления включены.",
            "subscription": "💳 <b>Подписка</b>\n\n🆓 Бесплатно: 5 просмотров/день\n💎 Премиум: безлимит за 50,000 сум/месяц",
            "statistics": "📊 <b>Статистика</b>\n\n📦 Объявлений: 5005\n🆕 Новых сегодня: 1604\n👥 Пользователей: 2341",
            "contacts": "📞 <b>Контакты</b>\n\n👨‍💼 Админ: @admin_yuk_uz\n🌐 yukuz.uz\n📧 info@yukuz.uz"
        }
        await callback.message.edit_text(texts[callback.data])
    await callback.answer()

@router.callback_query(F.data.in_(["how_to_use", "about_subscription", "contact_us", "rules"]))
async def help_submenu_callback(callback: CallbackQuery):
    """Help submenu handler"""
    if callback.data and callback.message:
        texts = {
            "how_to_use": "❓ <b>Как пользоваться</b>\n\n1. 🔍 Быстрый Поиск - найти груз\n2. 📦 Мои объявления - ваши посты\n3. ➕ Добавить - создать пост\n4. ⚙️ Настройки - язык, подписка\n5. ℹ️ Помощь - справка",
            "about_subscription": "💳 <b>О подписке</b>\n\n🆓 Бесплатно: 5 просмотров контактов в день\n💎 Премиум: безлимитный доступ\n💰 Цена: 50,000 сум/месяц",
            "contact_us": "📞 <b>Связаться с нами</b>\n\n👨‍💼 Админ: @admin_yuk_uz\n📱 Канал: @yuk_uz_news\n🌐 Сайт: yukuz.uz",
            "rules": "📋 <b>Правила</b>\n\n• Указывайте реальные данные\n• Не спамьте объявлениями\n• Будьте вежливы\n• Соблюдайте законы УЗ"
        }
        await callback.message.edit_text(texts[callback.data])
    await callback.answer()

@router.message(F.text == "📦 Мои объявления")
async def my_announcements_handler(message: Message):
    """My announcements handler - shows user's posts"""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Мои грузы")],
            [KeyboardButton(text="🚛 Мой транспорт")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("📦 <b>Мои объявления</b>", reply_markup=keyboard)

@router.message(F.text == "➕ Добавить объявление")
async def add_announcement_handler(message: Message):
    """Add announcement handler - goes to creation interface"""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Добавить груз")],
            [KeyboardButton(text="🚛 Добавить транспорт")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("➕ <b>Добавить объявление</b>", reply_markup=keyboard)

@router.message(F.text == "⚙️ Настройки")
async def settings_handler(message: Message):
    """Settings handler - goes to settings menu"""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌐 Изменить язык")],
            [KeyboardButton(text="🔔 Уведомления")],
            [KeyboardButton(text="💳 Подписка")],
            [KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="📞 Контакты")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("⚙️ <b>Настройки</b>", reply_markup=keyboard)

@router.message(F.text.in_(["Все", "Тент", "Реф", "маленький Исузу", "большой Исузу", "Чакман", "Камаз", "Мега", "Площадка", "Поровоз", "Трал", "Лабо", "Догруз", "Спринтер", "Другие"]))
async def vehicle_selection(message: Message, state: FSMContext):
    """Handle vehicle type selection"""
    vehicle_mapping = {
        "Все": "all",
        "Тент": "tent", 
        "Реф": "ref",
        "маленький Исузу": "small_isuzu",
        "большой Исузу": "big",
        "Чакман": "chakman",
        "Камаз": "kamaz",
        "Мега": "mega",
        "Площадка": "platform",
        "Поровоз": "train",
        "Трал": "tral",
        "Лабо": "labo",
        "Догруз": "dogruz",
        "Спринтер": "sprinter",
        "Другие": "other"
    }
    
    vehicle_type = vehicle_mapping.get(message.text, "all")
    await state.update_data(vehicle_filter=vehicle_type)
    
    await message.answer(f"🔄 <b>Тип транспорта выбран: {message.text}</b>")
    
    instructions = """Введите города для поиска грузов:

Примеры:

⏺ Toshkent
⏺ Москва
⏺ Toshkent Самарканд
⏺ Стамбул Olmata"""
    
    await message.answer(instructions)
    await state.set_state(SearchState.waiting_city_input)

@router.message(SearchState.waiting_city_input)
async def handle_city_search(message: Message, state: FSMContext):
    """Handle city search input"""
    if not message.text:
        await message.answer("❌ Пожалуйста, введите города для поиска")
        return
        
    data = await state.get_data()
    search_type = data.get("search_type", "cargo")
    vehicle_filter = data.get("vehicle_filter", "all")
    
    search_text = message.text.strip()
    logger.info(f"Search: {search_type}, filter: {vehicle_filter}, text: {search_text}")
    
    # Parse cities
    cities = search_text.replace("→", " ").replace("-", " ").split()
    from_city = cities[0] if cities else ""
    to_city = cities[1] if len(cities) > 1 else ""
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build query
        if search_type == "cargo":
            query = "SELECT * FROM announcements WHERE announcement_type = 'cargo'"
            conditions = []
            
            if vehicle_filter != "all":
                filter_terms = {
                    'tent': ['тент', 'tent'],
                    'ref': ['реф', 'ref'],
                    'small_isuzu': ['исузу', 'isuzu'],
                    'big': ['большой', 'big'],
                    'chakman': ['чакман'],
                    'kamaz': ['камаз', 'kamaz'],
                    'mega': ['мега', 'mega'],
                    'platform': ['площадка', 'платформа'],
                    'train': ['поровоз'],
                    'tral': ['трал'],
                    'labo': ['лабо'],
                    'dogruz': ['догруз'],
                    'sprinter': ['спринтер']
                }
                
                terms = filter_terms.get(vehicle_filter, [vehicle_filter])
                vehicle_conditions = []
                for term in terms:
                    vehicle_conditions.append(f"(LOWER(vehicle_type) LIKE '%{term}%' OR LOWER(cargo_type) LIKE '%{term}%' OR LOWER(description) LIKE '%{term}%')")
                
                if vehicle_conditions:
                    conditions.append(f"({' OR '.join(vehicle_conditions)})")
        else:
            query = "SELECT * FROM announcements WHERE announcement_type = 'transport'"
            conditions = []
        
        # Import comprehensive city database
        from app.city_database import get_city_variants
        
        # Smart city search with comprehensive variants
        if from_city:
            from_city_clean = from_city.lower().strip()
            
            # Get ALL possible variants including grammatical forms
            search_variants = get_city_variants(from_city_clean)
            from_conditions = []
            for variant in search_variants:
                from_conditions.append(f"LOWER(from_location) LIKE '%{variant.lower()}%'")
            conditions.append(f"({' OR '.join(from_conditions)})")
            
        if to_city:
            to_city_clean = to_city.lower().strip()
            
            # Get ALL possible variants for destination city
            search_variants = get_city_variants(to_city_clean)
            to_conditions = []
            for variant in search_variants:
                to_conditions.append(f"LOWER(to_location) LIKE '%{variant.lower()}%'")
            conditions.append(f"({' OR '.join(to_conditions)})")
        
        if conditions:
            query += " AND " + " AND ".join(conditions)
        
        query += " ORDER BY created_at DESC LIMIT 6"
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not results:
            await message.answer("❌ По вашему запросу ничего не найдено.")
            return
        
        # Send first 5 results as individual messages exactly like original
        for i, row in enumerate(results[:5], 1):
            # Unpack all 24 columns from database
            (announcement_id, title, description, ann_type, status, from_loc, to_loc, 
             weight, cargo_type, vehicle_type, contact_name, contact_phone, contact_address,
             notes, user_tg_id, user_name, location_lat, location_lon, created_at, updated_at, 
             expires_at, views_count, contacts_accessed, message_url) = row
            
            from_flag = get_country_flag(from_loc)
            to_flag = get_country_flag(to_loc)
            
            distance, travel_time = calculate_distance_and_time(from_loc, to_loc)
            time_ago = format_time_ago(created_at)
            
            # Exact format like in image: "1. 🇺🇿 Ангрен - 🇷🇺 Грозный"
            text = f"<b>{i}. {from_flag} {from_loc} - {to_flag} {to_loc}</b>\n\n"
            text += f"⚖️ {weight}\n"
            
            if vehicle_type:
                text += f"🚚 {vehicle_type}\n"
            
            if cargo_type:
                text += f"📦 {cargo_type}\n"
            
            if distance > 0:
                text += f"🛣️ {distance} км {travel_time:.1f} часов\n\n"
            
            text += time_ago
            
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Подробнее", callback_data=f"details:{announcement_id}")]
                ]
            )
            
            await message.answer(text, reply_markup=keyboard)
        
        # Get total count for summary
        count_query = "SELECT COUNT(*) FROM announcements WHERE status = 'published'"
        if conditions:
            count_query += " AND " + " AND ".join(conditions)
        
        cursor.execute(count_query)
        total_count = cursor.fetchone()[0]
        
        # Count today's announcements
        today_query = count_query + " AND DATE(created_at) = CURRENT_DATE"
        cursor.execute(today_query)
        today_count = cursor.fetchone()[0]
        
        # Summary message EXACTLY like in image: "🚚 Найдено 4883 объявлений, 728 из них сегодня"
        summary_text = f"🚚 Найдено {total_count} объявлений, {today_count} из них сегодня"
        await message.answer(summary_text)
        
        # Show pagination button if more results available
        if len(results) >= 5 and total_count > 5:
            summary_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=f"5 из {total_count} показать больше", callback_data=f"more:{vehicle_filter}:{from_city or ''}:{to_city or ''}:5")]
                ]
            )
            await message.answer("", reply_markup=summary_keyboard)
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        await message.answer("❌ Ошибка поиска. Попробуйте еще раз.")

@router.callback_query(F.data.startswith("details:"))
async def show_announcement_details(callback: CallbackQuery):
    """Show detailed view exactly like original"""
    if not callback.data:
        await callback.answer("❌ Ошибка данных")
        return
        
    announcement_id = callback.data.split(":")[1]
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get announcement details
        cursor.execute("SELECT * FROM announcements WHERE id = %s", (announcement_id,))
        row = cursor.fetchone()
        
        if not row:
            await callback.answer("❌ Объявление не найдено")
            return
        
        # Update views count
        cursor.execute("UPDATE announcements SET views_count = views_count + 1 WHERE id = %s", (announcement_id,))
        conn.commit()
        
        # Unpack all 24 columns from database  
        (announcement_id, title, description, ann_type, status, from_loc, to_loc, 
         weight, cargo_type, vehicle_type, contact_name, contact_phone, contact_address,
         notes, user_tg_id, user_name, location_lat, location_lon, created_at, updated_at, 
         expires_at, views, contacts, message_url) = row
        
        # Format exactly like the image from attached_assets/image_1755264553345.png
        text = f"<b>{contact_name}</b>\n\n"
        text += f"<b>{from_loc} - {to_loc}</b>\n\n"
        
        if cargo_type and cargo_type.strip():
            text += f"{cargo_type}\n\n"
        
        text += f"<b>Тонна: {weight}</b>\n\n"
        text += "Тел:\n\n"
        text += (description if description else "Описание отсутствует")
        text += f"\n\n👁 {views + 1} 📞 {contacts}"
        
        # Keyboard exactly like original - 3 buttons in exact layout from image
        keyboard_buttons = [
            [
                InlineKeyboardButton(text="📞 Номер телефона", callback_data=f"phone:{contact_phone}:{announcement_id}"),
                InlineKeyboardButton(text="💬 Перейти к сообщению", url=f"https://t.me/user?id={user_tg_id}" if user_tg_id else "https://t.me/uzlogistics_pro_bot")
            ],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
        ]
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        cursor.close()
        conn.close()
        
        if callback.message:
            await callback.message.answer(text, reply_markup=keyboard)
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error showing details: {e}")
        await callback.answer("❌ Ошибка загрузки данных")

@router.callback_query(F.data.startswith("phone:"))
async def show_phone_number(callback: CallbackQuery):
    """Show phone number and increment contact counter"""
    if not callback.data:
        await callback.answer("❌ Ошибка данных")
        return
        
    parts = callback.data.split(":")
    phone = parts[1]
    announcement_id = parts[2]
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update contacts accessed count
        cursor.execute("UPDATE announcements SET contacts_accessed = contacts_accessed + 1 WHERE id = %s", (announcement_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        await callback.answer(f"📞 Телефон: {phone}", show_alert=True)
        
    except Exception as e:
        logger.error(f"Error accessing phone: {e}")
        await callback.answer(f"📞 Телефон: {phone}", show_alert=True)

@router.callback_query(F.data.startswith("more:"))
async def show_more_results(callback: CallbackQuery):
    """Show more search results with pagination"""
    if not callback.data:
        await callback.answer("❌ Ошибка данных")
        return
        
    try:
        parts = callback.data.split(":")
        vehicle_filter = parts[1]
        from_city = parts[2] if parts[2] else None
        to_city = parts[3] if parts[3] else None
        offset = int(parts[4])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build query with same conditions as original search
        query = "SELECT * FROM announcements WHERE status = 'published'"
        conditions = []
        
        if vehicle_filter != "all":
            vehicle_conditions = []
            if vehicle_filter == "tent":
                vehicle_conditions = ["LOWER(vehicle_type) LIKE '%тент%'", "LOWER(vehicle_type) LIKE '%tent%'"]
            elif vehicle_filter == "ref":
                vehicle_conditions = ["LOWER(vehicle_type) LIKE '%реф%'", "LOWER(vehicle_type) LIKE '%ref%'"]
            
            if vehicle_conditions:
                conditions.append(f"({' OR '.join(vehicle_conditions)})")
        
        # Universal city search - works with ANY city name in the world  
        if from_city:
            from_city_clean = from_city.lower().strip()
            conditions.append(f"LOWER(from_location) LIKE '%{from_city_clean}%'")
            
        if to_city:
            to_city_clean = to_city.lower().strip()
            conditions.append(f"LOWER(to_location) LIKE '%{to_city_clean}%'")
        
        if conditions:
            query += " AND " + " AND ".join(conditions)
        
        query += f" ORDER BY created_at DESC LIMIT 5 OFFSET {offset}"
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            await callback.answer("❌ Больше результатов нет")
            return
        
        # Show next 5 results
        for i, row in enumerate(results, offset + 1):
            (announcement_id, title, description, ann_type, status, from_loc, to_loc, 
             weight, cargo_type, vehicle_type, contact_name, contact_phone, contact_address,
             notes, user_tg_id, user_name, location_lat, location_lon, created_at, updated_at, 
             expires_at, views_count, contacts_accessed, message_url) = row
            
            from_flag = get_country_flag(from_loc)
            to_flag = get_country_flag(to_loc)
            
            distance, travel_time = calculate_distance_and_time(from_loc, to_loc)
            time_ago = format_time_ago(created_at)
            
            text = f"<b>{i}. {from_flag} {from_loc} - {to_flag} {to_loc}</b>\n\n"
            text += f"⚖️ {weight}\n"
            
            if vehicle_type:
                text += f"🚚 {vehicle_type}\n"
            
            if cargo_type:
                text += f"📦 {cargo_type}\n"
            
            if distance > 0:
                text += f"🛣️ {distance} км {travel_time:.1f} часов\n\n"
            
            text += time_ago
            
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Подробнее", callback_data=f"details:{announcement_id}")]
                ]
            )
            
            await callback.message.answer(text, reply_markup=keyboard)
        
        # Show next pagination button if more results available
        next_offset = offset + 5
        count_query = "SELECT COUNT(*) FROM announcements WHERE status = 'published'"
        if conditions:
            count_query += " AND " + " AND ".join(conditions)
        
        cursor.execute(count_query)
        total_count = cursor.fetchone()[0]
        
        if next_offset < total_count:
            next_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=f"{next_offset} из {total_count} показать больше", callback_data=f"more:{vehicle_filter}:{from_city or ''}:{to_city or ''}:{next_offset}")]
                ]
            )
            await callback.message.answer(f"🔍 Показано {next_offset} из {total_count}", reply_markup=next_keyboard)
        
        cursor.close()
        conn.close()
        await callback.answer()
        
    except Exception as e:
        logger.error(f"More results error: {e}")
        await callback.answer("❌ Ошибка загрузки")
