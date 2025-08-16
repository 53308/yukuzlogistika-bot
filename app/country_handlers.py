# -*- coding: utf-8 -*-
"""
Country and City Selection Handlers for Search
Обработчики выбора стран и городов для поиска
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext

def get_uzbekistan_cities_keyboard(search_type: str) -> InlineKeyboardMarkup:
    """Get Uzbekistan cities keyboard exactly like original bot"""
    cities = [
        ("🏙️ Ташкент - 161", "city_tashkent"),
        ("🏭 Андижан - 57", "city_andijan"), 
        ("🏛️ Бухара - 17", "city_bukhara"),
        ("🌾 Галлаорол - 2", "city_gallaarol"),
        ("🌱 Гулистан - 1", "city_gulistan"),
        ("⚡ Денау - 3", "city_denau"),
        ("🏭 Джизак - 21", "city_jizzakh"),
        ("🏘️ Кашкадарья - 7", "city_kashkadarya"),
        ("🕌 Кокан - 21", "city_kokan"),
        ("💫 Косон - 1", "city_koson"),
        ("🌸 Мубарак - 2", "city_mubarak"),
        ("🌸 Навои - 9", "city_navoi"),
        ("🌻 Наманган - 43", "city_namangan"),
        ("🏛️ Нарпай - 2", "city_narpay"),
        ("🌿 Олтарик - 4", "city_oltarik"),
        ("🏙️ Самарканд - 34", "city_samarkand"),
        ("🏭 Сырдарья - 12", "city_syrdarya"),
        ("🌾 Термез - 2", "city_termez"),
        ("🏔️ Туракурган - 2", "city_turakurgan"),
        ("🌄 Ургенч - 1", "city_urgench"),
        ("🌸 Учкурган - 1", "city_uchkurgan"),
        ("🌻 Фергана - 14", "city_fergana"),
        ("🏛️ Хорезм - 5", "city_khorezm"),
        ("🌺 Шахрихон - 1", "city_shahrikhon"),
        ("🏞️ Янгийул - 1", "city_yangiyul"),
        ("🌿 прочие - 14", "city_others")
    ]
    
    keyboard = []
    for i in range(0, len(cities), 2):
        row = []
        for j in range(2):  # Maximum 2 buttons per row
            if i + j < len(cities):
                name, callback = cities[i + j]
                row.append(InlineKeyboardButton(
                    text=name, 
                    callback_data=f"{callback}_{search_type}"
                ))
        keyboard.append(row)
    
    # Add back button
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_countries_{search_type}")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_russia_cities_keyboard(search_type: str) -> InlineKeyboardMarkup:
    """Get Russia cities keyboard"""
    cities = [
        ("🏛️ Москва - 89", "city_moscow"),
        ("🌊 Санкт-Петербург - 12", "city_spb"),
        ("🌾 Грозный - 45", "city_grozny"),
        ("🏭 Казань - 23", "city_kazan"),
        ("🌸 Екатеринбург - 8", "city_ekaterinburg"),
        ("🌻 Новосибирск - 15", "city_novosibirsk"),
        ("⚡ Челябинск - 7", "city_chelyabinsk"),
        ("🌿 Уфа - 12", "city_ufa"),
        ("🌺 Ростов-на-Дону - 18", "city_rostov"),
        ("🏞️ Волгоград - 9", "city_volgograd"),
        ("🌱 Краснодар - 14", "city_krasnodar"),
        ("🏙️ Нижний Новгород - 6", "city_nn"),
        ("🌄 прочие - 22", "city_others_ru")
    ]
    
    keyboard = []
    for i in range(0, len(cities), 2):
        row = []
        for j in range(2):
            if i + j < len(cities):
                name, callback = cities[i + j]
                row.append(InlineKeyboardButton(
                    text=name,
                    callback_data=f"{callback}_{search_type}"
                ))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_countries_{search_type}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_kazakhstan_cities_keyboard(search_type: str) -> InlineKeyboardMarkup:
    """Get Kazakhstan cities keyboard"""
    cities = [
        ("🏙️ Алматы - 67", "city_almaty"),
        ("🌸 Астана - 23", "city_astana"),
        ("🌾 Шымкент - 18", "city_shymkent"),
        ("🏭 Караганда - 12", "city_karaganda"),
        ("🌻 Актобе - 8", "city_aktobe"),
        ("⚡ Павлодар - 6", "city_pavlodar"),
        ("🌿 прочие - 15", "city_others_kz")
    ]
    
    keyboard = []
    for i in range(0, len(cities), 2):
        row = []
        for j in range(2):
            if i + j < len(cities):
                name, callback = cities[i + j]
                row.append(InlineKeyboardButton(
                    text=name,
                    callback_data=f"{callback}_{search_type}"
                ))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_countries_{search_type}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def handle_country_selection(callback_query: CallbackQuery, state: FSMContext):
    """Handle country selection and show cities"""
    data = callback_query.data
    
    # Extract country and search type from callback data
    if "_cargo" in data:
        search_type = "cargo"
        country_code = data.replace("country_", "").replace("_cargo", "")
    else:
        search_type = "transport"
        country_code = data.replace("country_", "").replace("_transport", "")
    
    # Store search data
    await state.update_data(country=country_code, search_type=search_type)
    
    # Show cities based on country
    if country_code == "uz":
        keyboard = get_uzbekistan_cities_keyboard(search_type)
        country_name = "🇺🇿 Узбекистан"
        count = "498 объявлений, 91 из них сегодня"
    elif country_code == "ru":
        keyboard = get_russia_cities_keyboard(search_type)
        country_name = "🇷🇺 Россия"  
        count = "234 объявления, 45 из них сегодня"
    elif country_code == "kz":
        keyboard = get_kazakhstan_cities_keyboard(search_type)
        country_name = "🇰🇿 Казахстан"
        count = "156 объявлений, 28 из них сегодня"
    else:
        await callback_query.answer("Города для этой страны пока недоступны")
        return
    
    search_icon = "📦" if search_type == "cargo" else "🚚"
    search_text = "Найти груз" if search_type == "cargo" else "Найти транспорт"
    
    await callback_query.message.edit_text(
        f"🔍 <b>Быстрый Поиск</b>\n\n"
        f"{search_icon} <b>{search_text}</b>\n"
        f"{search_icon}⚡⚡⚡⚡ 13:00\n\n"
        f"{search_icon} <b>Найдено {count}</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def handle_city_selection(callback_query: CallbackQuery, state: FSMContext):
    """Handle city selection and perform search"""
    from app.routers.search import perform_search_by_city
    
    data = callback_query.data
    
    # Extract city and search type from callback data  
    if "_cargo" in data:
        search_type = "cargo"
        city_code = data.replace("city_", "").replace("_cargo", "")
    else:
        search_type = "transport" 
        city_code = data.replace("city_", "").replace("_transport", "")
    
    # Map city codes to actual city names for search
    city_mapping = {
        "tashkent": "Ташкент",
        "andijan": "Андижан", 
        "bukhara": "Бухара",
        "samarkand": "Самарканд",
        "namangan": "Наманган",
        "fergana": "Фергана",
        "jizzakh": "Жиззах",
        "moscow": "Москва",
        "grozny": "Грозный",
        "spb": "Санкт-Петербург",
        "kazan": "Казань",
        "almaty": "Алматы",
        "astana": "Астана",
        "shymkent": "Шымкент"
    }
    
    city_name = city_mapping.get(city_code, city_code.capitalize())
    
    await callback_query.answer(f"Ищу {search_type} в {city_name}...")
    
    # Perform search
    await perform_search_by_city(callback_query, city_name, search_type, state)
