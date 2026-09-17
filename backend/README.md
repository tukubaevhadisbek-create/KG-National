# Кыргыз Дүйнөсү — Backend

Django + DRF API для Telegram Mini App «Кыргыз Дүйнөсү».

## Установка

```bash
cd backend
python3 -m venv venv
. venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env         # затем впишите TELEGRAM_BOT_TOKEN и остальное
```

## Запуск (разработка, SQLite)

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Админ-панель: http://127.0.0.1:8000/admin/
API: http://127.0.0.1:8000/api/

## Наполнение тестовым контентом

Создайте через `/admin/`:
1. `Locations` → одну локацию, slug `uy`, name_ky `Үй`
2. `Categories` → например slug `uy-buyumdaru`, name_ky `Үй буюмдары`
3. `Items` → несколько предметов с этой локацией/категорией
4. `Quests` → задание "Чыныны тап." с `correct_item` и вариантами (`QuestOption`, инлайн в форме квеста)

## Проверка API вручную (без Telegram)

Реальный `initData` можно получить только из настоящего Telegram-клиента,
но для локальной проверки эндпоинтов, не требующих авторизации Telegram,
используйте `python manage.py shell` — пример полного сквозного сценария
(авторизация → discover → quest → progress) уже проверен и лежит в истории
разработки (см. пояснения в чате).

## Список API

| Метод | URL | Описание |
|---|---|---|
| POST | `/api/auth/telegram/` | Вход через Telegram initData, выдаёт JWT |
| POST | `/api/auth/refresh/` | Обновление access-токена |
| GET | `/api/profile/me/` | Профиль текущего пользователя |
| GET | `/api/locations/` | Список локаций |
| GET | `/api/categories/` | Список категорий |
| GET | `/api/items/?location=&category=` | Список предметов с фильтрами |
| GET | `/api/items/{id}/` | Детали предмета |
| POST | `/api/items/{id}/discover/` | Открыть предмет (тыйын + проверка достижений) |
| GET | `/api/quests/?location=` | Список заданий |
| POST | `/api/quests/{id}/answer/` | Ответ на задание (тыйын + проверка достижений) |
| GET | `/api/progress/me/` | Прогресс пользователя |
| GET | `/api/achievements/` | Список достижений с флагом is_unlocked |
| GET | `/api/furniture/?category=` | Каталог мебели для комнаты |
| POST | `/api/furniture/{id}/purchase/` | Купить мебель (списание тыйын) |
| GET | `/api/rooms/me/` | Текущая комната (фон + расставленная мебель) |
| PATCH | `/api/rooms/me/` | Сменить фон комнаты |

## Модели (по приложениям)

- **accounts** — `Profile`
- **worlds** — `Location`, `Category`
- **items** — `Item`
- **quests** — `Quest`, `QuestOption`, `QuestAttempt`
- **progress** — `UserProgress`, `DiscoveredItem`
- **rewards** — `RewardTransaction` (журнал тыйын — источник истины по балансу)
- **achievements** — `Achievement`, `UserAchievement`
- **rooms** — `Furniture`, `Room`, `UserFurniture`

## Защита игровой валюты (реализовано и протестировано)

- Frontend никогда не передаёт сумму тыйын — она всегда берётся из
  `Item.discover_reward` / `Quest.reward_coins` / `Furniture.price` на backend.
- Баланс меняется только через `apps.rewards.services.grant_reward()` /
  `spend_coins()`, под `select_for_update()` — гонки при одновременных
  запросах исключены.
- Повторное открытие предмета, повторный правильный ответ на квест и
  повторная покупка одной и той же мебели не дают повторную награду/списание.
- Покупка при нехватке тыйын отклоняется с кодом 402, до создания записи.

## Переход на PostgreSQL (продакшн)

Заполните в `.env`: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`,
`POSTGRES_HOST`, `POSTGRES_PORT` — settings.py автоматически переключится
с SQLite на PostgreSQL. После этого:

```bash
python manage.py migrate
```

## Следующие шаги (по плану)

- Этап 6 — реальное подключение Telegram Bot + WebApp кнопка
- Этап 7 — AI-помощник (акылдуу жардамчы) и распознавание речи
- Этап 8 — тестирование сценариев
