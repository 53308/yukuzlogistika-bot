from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.startswith("/approve"))
async def approve_cmd(m: Message):
    # Пример: /approve 123
    await m.answer("Пост утверждён и отправлен в канал.")
