from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

REGIONS = [
    "Ташкент", "Сырдарё", "Наманган", "Андижон", "Бухоро", "Фергана", "Самарканд", "Хоразм",
    "Қашқадарё", "Навоий", "Жиззах", "Қорақалпоғистон"
]

VEHICLES = ["Фура", "КамАЗ", "Isuzu", "Газель", "Тент", "Рефрижератор", "Контейнеровоз"]

# Main menu button texts by language
MAIN_MENU_TEXTS = {
    "uz": {
        "quick_search": "🗣 Tezkor Qidiruv",
        "my_listings": "📋 Mening e'lonlarim", 
        "add_listing": "➕ E'lon qo'shish",
        "settings": "⚙️ Sozlamalar",
        "help": "ℹ️ Yordam"
    },
    "uz_cyrillic": {
        "quick_search": "🗣 Тезкор Қидирув",
        "my_listings": "📋 Менинг эълонларим",
        "add_listing": "➕ Эълон қўшиш", 
        "settings": "⚙️ Созламалар",
        "help": "ℹ️ Ёрдам"
    },
    "ru": {
        "quick_search": "🗣 Быстрый поиск",
        "my_listings": "📋 Мои объявления",
        "add_listing": "➕ Добавить объявление",
        "settings": "⚙️ Настройки", 
        "help": "ℹ️ Помощь"
    }
}

def get_main_menu(language: str = "uz") -> ReplyKeyboardMarkup:
    """Get main menu keyboard for specified language"""
    if language not in MAIN_MENU_TEXTS:
        language = "uz"  # fallback
    
    texts = MAIN_MENU_TEXTS[language]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts["quick_search"]), KeyboardButton(text=texts["my_listings"])],
            [KeyboardButton(text=texts["add_listing"]), KeyboardButton(text=texts["settings"])],
            [KeyboardButton(text=texts["help"])],
        ], resize_keyboard=True
    )

# Default menu (for backward compatibility)
MAIN_MENU = get_main_menu("uz")

def get_button_type(button_text: str) -> str:
    """Determine button type from text regardless of language"""
    for lang, texts in MAIN_MENU_TEXTS.items():
        for button_type, text in texts.items():
            if text == button_text:
                return button_type
    return "unknown"

def get_language_menu() -> InlineKeyboardMarkup:
    """Get language selection keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha (Lotin)", callback_data="lang:uz")],
        [InlineKeyboardButton(text="🇺🇿 Ўзбекча (Кирилл)", callback_data="lang:uz_cyrillic")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
    ])

def get_quick_search_menu(language: str = "uz") -> InlineKeyboardMarkup:
    """Get quick search submenu keyboard"""
    if language == "uz":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📦 Yuk topish", callback_data="search:cargo")],
            [InlineKeyboardButton(text="🚛 Moshina topish", callback_data="search:transport")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="search:back")],
        ])
    elif language == "uz_cyrillic":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📦 Юк топиш", callback_data="search:cargo")],
            [InlineKeyboardButton(text="🚛 Мошина топиш", callback_data="search:transport")],
            [InlineKeyboardButton(text="🔙 Орқага", callback_data="search:back")],
        ])
    else:  # Russian
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📦 Поиск груза", callback_data="search:cargo")],
            [InlineKeyboardButton(text="🚛 Поиск машины", callback_data="search:transport")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="search:back")],
        ])

def regions_kb() -> InlineKeyboardMarkup:
    rows = []
    row = []
    for i, r in enumerate(REGIONS, start=1):
        row.append(InlineKeyboardButton(text=r, callback_data=f"region:{r}"))
        if i % 3 == 0:
            rows.append(row); row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(inline_keyboard=rows)

def vehicles_kb() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=v, callback_data=f"vehicle:{v}")] for v in VEHICLES]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def post_type_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Груз", callback_data="type:load")],
        [InlineKeyboardButton(text="🚛 Машина", callback_data="type:truck")],
    ])
