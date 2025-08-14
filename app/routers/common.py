from aiogram import Router, F
from aiogram.types import Message
from ..keyboards import MAIN_MENU, post_type_kb
from ..texts import HELP

router = Router()

@router.message(F.text == "/start")
@router.message(F.text == "ℹ️ Помощь")
@router.message(F.text == "/help")
async def cmd_start(message: Message):
    await message.answer(
        "Assalomu alaykum! Bu logistika boti. Tanlang:", reply_markup=MAIN_MENU
    )
    await message.answer(HELP)

@router.message(F.text == "➕ Новое объявление")
@router.message(F.text == "/new")
async def new_post(message: Message):
    await message.answer("Выберите тип объявления:", reply_markup=post_type_kb())
