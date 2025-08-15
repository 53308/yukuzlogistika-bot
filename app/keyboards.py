from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

REGIONS = [
    "Ташкент", "Сырдарё", "Наманган", "Андижон", "Бухоро", "Фергана", "Самарканд", "Хоразм",
    "Қашқадарё", "Навоий", "Жиззах", "Қорақалпоғистон"
]

VEHICLES = ["Фура", "КамАЗ", "Isuzu", "Газель", "Тент", "Рефрижератор", "Контейнеровоз"]

MAIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🗣 Тезkor Qidiruv"), KeyboardButton(text="📋 Mening e'lonlarim")],
        [KeyboardButton(text="➕ E'lon qo'shish"), KeyboardButton(text="⚙️ Sozlamalar")],
        [KeyboardButton(text="❓ Помощь")],
    ], resize_keyboard=True
)

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
