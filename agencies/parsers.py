"""
Парсеры внешних рейтингов агентств с карт.

— 2ГИС: Catalog API (нужен ключ GIS_2GIS_API_KEY).
— Яндекс.Карты: Geosearch API находит карточку (нужен YANDEX_GEOSEARCH_API_KEY),
  затем скрейп страницы для извлечения рейтинга из JSON-LD.
— Google Maps: автоматический парсинг невозможен без платного Places API,
  поэтому функция возвращает None и ожидает ручного ввода.

Все функции возвращают dict {rating, count, url} или None, ничего не бросают.
"""

import json
import logging
import re
import time
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

REQUEST_TIMEOUT = 10


_REGION_2GIS = {
    "Москва": 32, "Санкт-Петербург": 38, "Новосибирск": 1, "Екатеринбург": 54,
    "Казань": 41, "Нижний Новгород": 50, "Челябинск": 60, "Самара": 61,
    "Омск": 66, "Ростов-на-Дону": 39, "Уфа": 43, "Красноярск": 9,
    "Воронеж": 49, "Пермь": 48, "Волгоград": 47, "Краснодар": 33,
}


def _http_json(url, params=None, timeout=REQUEST_TIMEOUT):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Accept-Language": "ru-RU,ru;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _http_text(url, timeout=REQUEST_TIMEOUT):
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "ru-RU,ru;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="ignore")


def fetch_2gis(name, city, address=""):
    """
    Возвращает {rating, count, url} или None.
    Документация: https://docs.2gis.com/ru/api/search/catalog/reference
    """
    key = settings.GIS_2GIS_API_KEY
    if not key:
        logger.warning("GIS_2GIS_API_KEY не задан")
        return None

    region_id = _REGION_2GIS.get(city)
    params = {
        "q": f"{name} {city}".strip(),
        "fields": "items.point,items.reviews,items.name,items.address_name,items.id",
        "key": key,
        "page_size": 5,
    }
    if region_id:
        params["region_id"] = region_id

    try:
        data = _http_json("https://catalog.api.2gis.com/3.0/items", params)
    except Exception as e:
        logger.warning("2GIS request failed: %s", e)
        return None

    items = data.get("result", {}).get("items", [])
    if not items:
        return None

    # выбираем первый, где есть отзывы и название совпадает по первому слову
    first_word = name.split()[0].lower() if name.split() else ""
    best = None
    for it in items:
        nm = (it.get("name") or "").lower()
        if first_word and first_word not in nm:
            continue
        reviews = it.get("reviews") or {}
        if reviews.get("general_rating"):
            best = it
            break
    if not best:
        best = items[0]

    reviews = best.get("reviews") or {}
    rating = reviews.get("general_rating")
    count = reviews.get("general_review_count") or reviews.get("count")
    item_id = best.get("id")
    url = f"https://2gis.ru/firm/{item_id}" if item_id else ""
    if rating is None:
        return None
    return {"rating": float(rating), "count": int(count or 0), "url": url}


def fetch_yandex(name, city, address=""):
    """
    Двухшаговая стратегия:
      1) Yandex Geosearch API ищет карточку → получаем URL.
      2) Скрейпим страницу карточки, извлекаем рейтинг из JSON-LD.
    Шаг 2 нестабилен — Яндекс защищает страницы от ботов; иногда работает.
    """
    key = settings.YANDEX_GEOSEARCH_API_KEY
    if not key:
        logger.warning("YANDEX_GEOSEARCH_API_KEY не задан")
        return None

    params = {
        "apikey": key,
        "text": f"{name} {city}".strip(),
        "type": "biz",
        "results": 5,
        "lang": "ru_RU",
        "format": "json",
    }
    try:
        data = _http_json("https://search-maps.yandex.ru/v1/", params)
    except Exception as e:
        logger.warning("Yandex geosearch failed: %s", e)
        return None

    features = data.get("features") or []
    if not features:
        return None

    first_word = name.split()[0].lower() if name.split() else ""
    chosen = None
    for f in features:
        meta = (f.get("properties") or {}).get("CompanyMetaData") or {}
        nm = (meta.get("name") or "").lower()
        if first_word and first_word in nm:
            chosen = meta
            break
    if not chosen:
        chosen = (features[0].get("properties") or {}).get("CompanyMetaData") or {}

    url = chosen.get("url") or ""
    yandex_id = chosen.get("id")
    map_url = f"https://yandex.ru/maps/org/{yandex_id}/" if yandex_id else url

    # Скрейпим страницу — best-effort
    rating = None
    count = None
    if map_url:
        try:
            time.sleep(0.6)
            html = _http_text(map_url)
            # JSON-LD блок aggregateRating
            for m in re.finditer(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.S):
                try:
                    blob = json.loads(m.group(1))
                except Exception:
                    continue
                blobs = blob if isinstance(blob, list) else [blob]
                for b in blobs:
                    ar = b.get("aggregateRating") if isinstance(b, dict) else None
                    if ar:
                        rating = float(ar.get("ratingValue") or 0) or None
                        count = int(ar.get("ratingCount") or ar.get("reviewCount") or 0) or None
                        break
                if rating:
                    break
            # Фоллбэк: микроразметка в тексте
            if rating is None:
                rm = re.search(r'"ratingValue"\s*:\s*"?([\d.]+)"?', html)
                cm = re.search(r'"reviewCount"\s*:\s*"?(\d+)"?', html)
                if rm:
                    rating = float(rm.group(1))
                if cm:
                    count = int(cm.group(1))
        except Exception as e:
            logger.warning("Yandex page scrape failed: %s", e)

    if rating is None:
        # Если рейтинг не извлечь — всё равно вернём URL, чтобы можно было дозаполнить вручную
        if map_url:
            return {"rating": None, "count": None, "url": map_url}
        return None
    return {"rating": rating, "count": count, "url": map_url}


def fetch_google(name, city, address=""):
    """
    Полноценный парсинг Google Maps без Places API ($) практически невозможен.
    Заглушка для совместимости — поля заполняются админом вручную.
    """
    return None


PARSERS = {
    "2gis": fetch_2gis,
    "yandex": fetch_yandex,
    "google": fetch_google,
}
