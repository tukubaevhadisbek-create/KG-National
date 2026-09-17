"""
Проверка подлинности данных, которые Telegram Mini App передаёт
в window.Telegram.WebApp.initData.

Алгоритм официальный (описан в документации Telegram Bot API,
раздел "Validating data received via the Mini App"):

1. Разбираем initData как query string.
2. Забираем поле hash и удаляем его из данных.
3. Оставшиеся пары сортируем по ключу и склеиваем в
   "key=value" через "\n" — это data_check_string.
4. secret_key = HMAC_SHA256(bot_token, key="WebAppData")
5. вычисляем HMAC_SHA256(data_check_string, key=secret_key)
6. сравниваем с hash. Если не совпало — данные подделаны
   или устарели, доверять им нельзя.

Мы НИКОГДА не создаём пользователя и не начисляем тыйын на основе
данных, которые не прошли эту проверку.
"""

import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

from django.conf import settings


class TelegramAuthError(Exception):
    """Ошибка проверки подлинности initData."""


def _build_secret_key(bot_token: str) -> bytes:
    return hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()


def verify_telegram_init_data(init_data: str, max_age_seconds: int = 86400) -> dict:
    """
    Проверяет initData и возвращает словарь с распарсенными полями
    (в т.ч. 'user' уже как dict). Бросает TelegramAuthError, если
    данные не прошли проверку.
    """
    if not init_data:
        raise TelegramAuthError("initData бош болушу мүмкүн эмес")

    pairs = dict(parse_qsl(init_data, strict_parsing=True))

    received_hash = pairs.pop("hash", None)
    if not received_hash:
        raise TelegramAuthError("hash талаасы жок")

    data_check_string = "\n".join(
        f"{key}={value}" for key, value in sorted(pairs.items())
    )

    secret_key = _build_secret_key(settings.TELEGRAM_BOT_TOKEN)
    computed_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(computed_hash, received_hash):
        raise TelegramAuthError("initData жасалма же бурмаланган")

    auth_date = pairs.get("auth_date")
    if auth_date is not None:
        age = time.time() - int(auth_date)
        if age > max_age_seconds:
            raise TelegramAuthError("initData мөөнөтү өтүп кеткен")

    if "user" in pairs:
        pairs["user"] = json.loads(pairs["user"])

    return pairs
