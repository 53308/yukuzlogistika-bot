# yulogi-bot — Telegram логистика (aiogram v3)

Бот для объявлений по грузам и транспорту (Узбекистан). Потоки: «Груз» и «Машина», предпросмотр, поиск-заглушка, модерация-заглушка.

## Быстрый старт (локально)
1. Установите Python 3.10+.
2. Скопируйте `.env.example` в `.env` и заполните `BOT_TOKEN` (и при необходимости `CHANNEL_ID`).
3. Установите зависимости и запустите:
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

## Переменные окружения
- `BOT_TOKEN` — токен бота от @BotFather.
- `ADMINS` — id админов через запятую (опционально).
- `CHANNEL_ID` — id канала (формат -100…), если нужен автопостинг (заглушка).
- `DATABASE_URL` — по умолчанию `sqlite+aiosqlite:///./app/data.db`.

## Docker (опционально)
```bash
docker build -t yulogi-bot .
docker run --name yulogi --env-file .env --restart unless-stopped yulogi-bot
```
