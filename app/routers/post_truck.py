from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from ..keyboards import regions_kb, vehicles_kb
from ..texts import POST_TEMPLATE_TRUCK

router = Router()

class TruckForm(StatesGroup):
    region_from = State()
    region_to = State()
    vehicle = State()
    capacity = State()
    cargo = State()
    price = State()
    phone = State()
    hashtags = State()
    confirm = State()

@router.callback_query(F.data == "type:truck")
async def truck_start_cb(c: CallbackQuery, state: FSMContext):
    await state.set_state(TruckForm.region_from)
    await c.message.answer("Откуда вы готовы принять груз?", reply_markup=regions_kb())

@router.callback_query(F.data.startswith("region:"), TruckForm.region_from)
async def truck_from_cb(c: CallbackQuery, state: FSMContext):
    await state.update_data(region_from=c.data.split(":",1)[1])
    await state.set_state(TruckForm.region_to)
    await c.message.edit_text("Куда планируете?")

@router.callback_query(F.data.startswith("region:"), TruckForm.region_to)
async def truck_to_cb(c: CallbackQuery, state: FSMContext):
    await state.update_data(region_to=c.data.split(":",1)[1])
    await state.set_state(TruckForm.vehicle)
    await c.message.edit_text("Какое ТС?", reply_markup=vehicles_kb())

@router.callback_query(F.data.startswith("vehicle:"), TruckForm.vehicle)
async def truck_vehicle(c: CallbackQuery, state: FSMContext):
    await state.update_data(vehicle=c.data.split(":",1)[1])
    await state.set_state(TruckForm.capacity)
    await c.message.edit_text("Свободный тоннаж/объём?")

@router.message(TruckForm.capacity)
async def truck_capacity(m: Message, state: FSMContext):
    await state.update_data(capacity=m.text.strip())
    await state.set_state(TruckForm.cargo)
    await m.answer("Какой груз рассматриваете?")

@router.message(TruckForm.cargo)
async def truck_cargo(m: Message, state: FSMContext):
    await state.update_data(cargo=m.text.strip())
    await state.set_state(TruckForm.price)
    await m.answer("Цена/ставка?")

@router.message(TruckForm.price)
async def truck_price(m: Message, state: FSMContext):
    await state.update_data(price=m.text.strip())
    await state.set_state(TruckForm.phone)
    await m.answer("Телефон?")

@router.message(TruckForm.phone)
async def truck_phone(m: Message, state: FSMContext):
    await state.update_data(phone=m.text.strip())
    await state.set_state(TruckForm.hashtags)
    await m.answer("Хештеги: #город #регион")

@router.message(TruckForm.hashtags)
async def truck_hashtags(m: Message, state: FSMContext):
    await state.update_data(hashtags=m.text.strip())
    data = await state.get_data()
    text = POST_TEMPLATE_TRUCK.format(
        from_=data['region_from'], to=data['region_to'], vehicle=data['vehicle'],
        capacity=data['capacity'], cargo=data['cargo'], price=data['price'],
        phone=data['phone'], hashtags=data['hashtags']
    )
    await state.set_state(TruckForm.confirm)
    await m.answer("Проверьте объявление:\n\n" + text + "\n\nОтправить? (да/нет)")

@router.message(TruckForm.confirm, F.text.casefold().in_({"да","ha","xa","yes"}))
async def truck_submit(m: Message, state: FSMContext):
    await m.answer("✅ Объявление отправлено на модерацию.")
    await state.clear()

@router.message(TruckForm.confirm)
async def truck_cancel(m: Message, state: FSMContext):
    await m.answer("❌ Отменено.")
    await state.clear()
