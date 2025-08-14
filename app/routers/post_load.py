from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from ..keyboards import regions_kb, vehicles_kb
from ..texts import POST_TEMPLATE_LOAD

router = Router()

class LoadForm(StatesGroup):
    region_from = State()
    region_to = State()
    cargo = State()
    vehicle = State()
    capacity = State()
    price = State()
    phone = State()
    hashtags = State()
    confirm = State()

@router.callback_query(F.data == "type:load")
async def load_start_cb(c: CallbackQuery, state: FSMContext):
    await state.set_state(LoadForm.region_from)
    await c.message.answer("Откуда отправляем?", reply_markup=regions_kb())

@router.callback_query(F.data.startswith("region:"), LoadForm.region_from)
async def load_from_cb(c: CallbackQuery, state: FSMContext):
    await state.update_data(region_from=c.data.split(":",1)[1])
    await state.set_state(LoadForm.region_to)
    await c.message.edit_text("Куда?", reply_markup=regions_kb())

@router.callback_query(F.data.startswith("region:"), LoadForm.region_to)
async def load_to_cb(c: CallbackQuery, state: FSMContext):
    await state.update_data(region_to=c.data.split(":",1)[1])
    await state.set_state(LoadForm.cargo)
    await c.message.edit_text("Что за груз? (кратко)")

@router.message(LoadForm.cargo)
async def load_cargo(m: Message, state: FSMContext):
    await state.update_data(cargo=m.text.strip())
    await state.set_state(LoadForm.vehicle)
    await m.answer("Какая машина нужна?", reply_markup=vehicles_kb())

@router.callback_query(F.data.startswith("vehicle:"), LoadForm.vehicle)
async def load_vehicle(c: CallbackQuery, state: FSMContext):
    await state.update_data(vehicle=c.data.split(":",1)[1])
    await state.set_state(LoadForm.capacity)
    await c.message.edit_text("Тоннаж/объём?")

@router.message(LoadForm.capacity)
async def load_capacity(m: Message, state: FSMContext):
    await state.update_data(capacity=m.text.strip())
    await state.set_state(LoadForm.price)
    await m.answer("Цена (или 'договорная')?")

@router.message(LoadForm.price)
async def load_price(m: Message, state: FSMContext):
    await state.update_data(price=m.text.strip())
    await state.set_state(LoadForm.phone)
    await m.answer("Телефон для связи?")

@router.message(LoadForm.phone)
async def load_phone(m: Message, state: FSMContext):
    await state.update_data(phone=m.text.strip())
    await state.set_state(LoadForm.hashtags)
    await m.answer("Хештеги (регион/город), пример: #ЯНГИЕР #СЫРДАРЁ")

@router.message(LoadForm.hashtags)
async def load_hashtags(m: Message, state: FSMContext):
    await state.update_data(hashtags=m.text.strip())
    await state.set_state(LoadForm.confirm)
    data = await state.get_data()
    text = POST_TEMPLATE_LOAD.format(
        from_=data['region_from'], to=data['region_to'], cargo=data['cargo'],
        vehicle=data['vehicle'], capacity=data['capacity'], price=data['price'],
        phone=data['phone'], hashtags=data['hashtags']
    )
    await m.answer("Проверьте объявление:\n\n" + text + "\n\nОтправить? (да/нет)")

@router.message(LoadForm.confirm, F.text.casefold().in_({"да","ha","xa","yes"}))
async def load_submit(m: Message, state: FSMContext):
    # TODO: сохранить в БД и/или отправить в канал
    await m.answer("✅ Объявление отправлено на модерацию.")
    await state.clear()

@router.message(LoadForm.confirm)
async def load_cancel(m: Message, state: FSMContext):
    await m.answer("❌ Отменено.")
    await state.clear()
