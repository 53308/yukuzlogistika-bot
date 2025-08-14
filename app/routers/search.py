from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "🔎 Поиск")
@router.message(F.text == "/find")
async def search_entry(m: Message):
    await m.answer("Напишите запрос: пример — `Сырдарё → Янгийер`, `Isuzu 5т`, `#ЯНГИЕР`", parse_mode="Markdown")

@router.message()
async def search_free_text(m: Message):
    # Заглушка: в реальности — SQL LIKE по нужным колонкам
    q = m.text.strip()
    await m.answer(f"Результаты по запросу: {q}\n(Тут будут найденные объявления)")
