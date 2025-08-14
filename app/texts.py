"""
Multilingual texts for all bot features
Complete language support for Uzbek Latin, Uzbek Cyrillic, and Russian
"""

MULTILINGUAL_TEXTS = {
    # Uzbek Latin
    "uz": {
        "start_welcome": "🎯 <b>Yukuz Logistics Bot</b>ga xush kelibsiz!\n\n📦 Yuk va transport e'lonlari uchun bot",
        "language_selected": "🇺🇿 Til tanlandi: O'zbek tili (Lotin)",
        "help_message": "ℹ️ <b>Yordam</b>\n\nBot imkoniyatlari:\n• 📦 Yuk e'loni qo'shish\n• 🚛 Transport e'loni qo'shish\n• 🔍 E'lonlarni qidirish",
        "main_menu": "📋 Asosiy menyu",
        "quick_search_menu": "🔍 Tezkor qidiruv\n\nKerakli bo'limni tanlang:",
        "cargo_search_title": "📦 Yuk topish",
        "transport_search_title": "🚛 Moshina topish",
        "subscription_notice": "E'lonning telefon raqamini ko'rish uchun botimizga obuna bo'lish kerak.\nObuna xarid qilish uchun - quyidagi obuna turlari ko'rsatilgan tugmalardan birini bosing.\n\n❓Savollar yoki yordam uchun @marina_laty bilan bog'laning.",
        "no_announcements": "📭 Hozirda e'lonlar mavjud emas.",
        "subscription_required": "🔒 Kontaktlarni ko'rish uchun obuna kerak",
        "contact_sender": "💬 Yuboruvchi bilan bog'lanish",
        "contact_sender_desc": "Kontakt ma'lumotlari va to'g'ridan-to'g'ri xabarlar faqat obunachilarga ochiq.",
        "subscription_access_denied": "🔒 Kontaktlarni ko'rish uchun obuna kerak\n🔒 To'g'ridan-to'g'ri xabarlar faqat obunachilarga",
        "detailed_view": "Batafsil",
        "back": "🔙 Orqaga",
        "phone_number": "📞 Telefon raqami",
        "go_to_message": "💬 Xabarga o'tish",
        "subscribe": "📊 Obuna bo'lish",
        "1month_sub": "1 oylik obuna",
        "3month_sub": "3 oylik obuna", 
        "3day_sub": "3 kunlik obuna",
        "listings_found": "ta e'lon topildi",
        "today_listings": "tasi bugungi",
        "weight": "Og'irligi",
        "transport_type": "Transport turi",
        "price": "Narx",
        "distance_time": "Masofa va vaqt",
        "posted_time": "E'lon vaqti",
        "min_ago": "min oldin",
        "hour_ago": "soat oldin",
        "error_occurred": "❌ Xatolik yuz berdi",
        "cargo_description": "Yuk tavsifi",
        "route": "Marshrut",
        "contact_info": "Aloqa ma'lumotlari",
        "direct_message": "To'g'ridan-to'g'ri xabar",
        "subscription_prices": "Obuna narxlari:\n• 3 kun - 20,000 so'm\n• 1 oy - 60,000 so'm\n• 3 oy - 150,000 so'm",
        "free_contacts_remaining": "🆓 Bepul kontakt murojaatlari qolgan: {}/5",
        "free_contacts_exhausted": "🔒 Bepul kontakt murojaatlari tugadi (5/5)\n💰 Obuna sotib oling yoki keyingi kunni kuting",
        "contact_access_system_owner": "👑 Cheksiz kirish (tizim egasi)",
        "contact_access_subscriber": "✅ Sizda faol obuna bor",
        "contact_access_free": "🆓 Bepul kontakt murojaati ishlatildi ({}/5)"
    },
    
    # Uzbek Cyrillic
    "uz_cyrillic": {
        "start_welcome": "🎯 <b>Yukuz Logistics Bot</b>га хуш келибсиз!\n\n📦 Юк ва транспорт эълонлари учун бот",
        "language_selected": "🇺🇿 Тил танланди: Ўзбек тили (Кирилл)",
        "help_message": "ℹ️ <b>Ёрдам</b>\n\nБот имкониятлари:\n• 📦 Юк эълони қўшиш\n• 🚛 Транспорт эълони қўшиш\n• 🔍 Эълонларни қидириш",
        "main_menu": "📋 Асосий меню",
        "quick_search_menu": "🔍 Тезкор қидирув\n\nКеракли бўлимни танланг:",
        "cargo_search_title": "📦 Юк топиш",
        "transport_search_title": "🚛 Мошина топиш",
        "subscription_notice": "Эълоннинг телефон рақамини кўриш учун ботимизга обуна бўлиш керак.\nОбуна харид қилиш учун - қуйидаги обуна турлари кўрсатилган тугмалардан бирини босинг.\n\n❓Саволлар ёки ёрдам учун @marina_laty билан боғланинг.",
        "no_announcements": "📭 Ҳозирда эълонлар мавжуд эмас.",
        "subscription_required": "🔒 Контактларни кўриш учун обуна керак",
        "contact_sender": "💬 Юборувчи билан боғланиш", 
        "contact_sender_desc": "Контакт маълумотлари ва тўғридан-тўғри хабарлар фақат обуначиларга очиқ.",
        "subscription_access_denied": "🔒 Контактларни кўриш учун обуна керак\n🔒 Тўғридан-тўғри хабарлар фақат обуначиларга",
        "detailed_view": "Батафсил",
        "back": "🔙 Орқага",
        "phone_number": "📞 Телефон рақами",
        "go_to_message": "💬 Хабарга ўтиш",
        "subscribe": "📊 Обуна бўлиш",
        "1month_sub": "1 ойлик обуна",
        "3month_sub": "3 ойлик обуна",
        "3day_sub": "3 кунлик обуна",
        "listings_found": "та эълон топилди",
        "today_listings": "таси бугунги",
        "weight": "Оғирлиги",
        "transport_type": "Транспорт тури",
        "price": "Нарх",
        "distance_time": "Масофа ва вақт",
        "posted_time": "Эълон вақти",
        "min_ago": "мин олдин",
        "hour_ago": "соат олдин",
        "error_occurred": "❌ Хатолик юз берди",
        "cargo_description": "Юк тавсифи",
        "route": "Маршрут",
        "contact_info": "Алоқа маълумотлари",
        "direct_message": "Тўғридан-тўғри хабар",
        "subscription_prices": "Обуна нархлари:\n• 3 кун - 20,000 сўм\n• 1 ой - 60,000 сўм\n• 3 ой - 150,000 сўм"
    },
    
    # Russian
    "ru": {
        "start_welcome": "🎯 <b>Добро пожаловать в Yukuz Logistics Bot!</b>\n\n📦 Бот для объявлений о грузах и транспорте",
        "language_selected": "🇷🇺 Выбран язык: Русский",
        "help_message": "ℹ️ <b>Помощь</b>\n\nВозможности бота:\n• 📦 Добавить объявление о грузе\n• 🚛 Добавить объявление о транспорте\n• 🔍 Поиск объявлений",
        "main_menu": "📋 Главное меню",
        "quick_search_menu": "🔍 Быстрый поиск\n\nВыберите нужный раздел:",
        "cargo_search_title": "📦 Поиск груза",
        "transport_search_title": "🚛 Поиск машины",
        "subscription_notice": "Для просмотра телефонного номера в объявлении необходимо подписаться на нашего бота.\nДля покупки подписки - нажмите одну из кнопок ниже, где указаны типы подписок.\n\n❓Вопросы или помощь обращайтесь к @marina_laty",
        "no_announcements": "📭 Объявлений пока нет.",
        "subscription_required": "🔒 Для просмотра контактов нужна подписка",
        "contact_sender": "💬 Связаться с отправителем",
        "contact_sender_desc": "Контактная информация и прямые сообщения доступны только подписчикам.",
        "subscription_access_denied": "🔒 Для просмотра контактов нужна подписка\n🔒 Прямые сообщения доступны только подписчикам",
        "detailed_view": "Подробно",
        "back": "🔙 Назад",
        "phone_number": "📞 Номер телефона",
        "go_to_message": "💬 Перейти к сообщению",
        "subscribe": "📊 Подписаться",
        "1month_sub": "1 месячная подписка",
        "3month_sub": "3 месячная подписка",
        "3day_sub": "3 дневная подписка",
        "listings_found": "объявлений найдено",
        "today_listings": "сегодняшних",
        "weight": "Вес",
        "transport_type": "Тип транспорта",
        "price": "Цена",
        "distance_time": "Расстояние и время",
        "posted_time": "Время размещения",
        "min_ago": "мин назад",
        "hour_ago": "час назад",
        "error_occurred": "❌ Произошла ошибка",
        "cargo_description": "Описание груза",
        "route": "Маршрут",
        "contact_info": "Контактная информация",
        "direct_message": "Прямое сообщение",
        "subscription_prices": "Цены на подписку:\n• 3 дня - 20,000 сум\n• 1 месяц - 60,000 сум\n• 3 месяца - 150,000 сум",
        "free_contacts_remaining": "🆓 Бесплатных обращений к контактам: {}/5",
        "free_contacts_exhausted": "🔒 Бесплатные обращения к контактам закончились (5/5)\n💰 Приобретите подписку или ждите следующий день",
        "contact_access_system_owner": "👑 Безлимитный доступ (владелец системы)",
        "contact_access_subscriber": "✅ У вас активная подписка",
        "contact_access_free": "🆓 Использовано бесплатное обращение к контакту ({}/5)"
    }
}

def get_multilingual_text(key: str, language: str) -> str:
    """Get text in the specified language"""
    if language in MULTILINGUAL_TEXTS and key in MULTILINGUAL_TEXTS[language]:
        return MULTILINGUAL_TEXTS[language][key]
    
    # Fallback to Uzbek if language not found
    if key in MULTILINGUAL_TEXTS["uz"]:
        return MULTILINGUAL_TEXTS["uz"][key]
    
    return f"[{key}]"  # Return key if text not found

# Uzbek texts (for backward compatibility)
TEXTS_UZ = MULTILINGUAL_TEXTS["uz"]

# Russian texts (for backward compatibility)  
TEXTS_RU = MULTILINGUAL_TEXTS["ru"]

def format_listing_text(listing, language: str, index: int) -> str:
    """Format listing with proper language support"""
    text = f"{index}. 🇺🇿 {listing.origin} - 🇺🇿 {listing.destination}\n\n"
    
    # Weight
    if hasattr(listing, 'weight') and listing.weight:
        weight_label = get_multilingual_text("weight", language)
        text += f"⚖️ {weight_label}: {listing.weight}\n"
    
    # Transport type
    transport_label = get_multilingual_text("transport_type", language)
    transport_type = getattr(listing, 'cargo_type', 'Tent')
    text += f"🚚 {transport_label}: {transport_type}\n"
    
    # Description (short)
    if hasattr(listing, 'description') and listing.description:
        desc_label = get_multilingual_text("cargo_description", language)
        desc = listing.description[:30] + "..." if len(listing.description) > 30 else listing.description
        text += f"📦 {desc_label}: {desc}\n"
    
    # Price
    if hasattr(listing, 'price') and listing.price:
        price_label = get_multilingual_text("price", language)
        text += f"💵 {price_label}: {listing.price}\n"
    
    # Distance and time
    distance_label = get_multilingual_text("distance_time", language)
    text += f"🛣️ {distance_label}: 345 km 6.1 " + ("soatlik" if language == "uz" else "соатлик" if language == "uz_cyrillic" else "часа") + "\n"
    
    # Time posted
    from datetime import datetime
    time_diff = datetime.now() - listing.date_posted
    time_label = get_multilingual_text("posted_time", language)
    
    if time_diff.seconds < 3600:
        min_ago = get_multilingual_text("min_ago", language)
        time_text = f"{time_diff.seconds // 60} {min_ago}"
    else:
        hour_ago = get_multilingual_text("hour_ago", language)
        time_text = f"{time_diff.seconds // 3600} {hour_ago}"
    
    text += f"⏳ {time_text}"
    
    return text
