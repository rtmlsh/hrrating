"""
python manage.py geocode_agencies
Геокодирует адреса агентств через Nominatim (OpenStreetMap) и сохраняет
координаты в поля map_lat / map_lon.
"""
import time
import ssl
import urllib.request
import urllib.parse
import json
from django.core.management.base import BaseCommand
from agencies.models import Agency

# macOS не доверяет CA-бандлу Python по умолчанию
_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE


import re


def _clean_address(address):
    """
    Упрощает адрес для геокодинга:
    - убирает «офис …», «этаж …», «БЦ "…"», «корп. X», «стр. X» с их значениями
    - раскрывает частые сокращения (пр-т → проспект, б-р → бульвар и т.д.)
    """
    addr = address

    # убрать "офис 301", "оф. 301", "этаж 5", "эт. 5" вместе с числом/буквой
    addr = re.sub(r',?\s*(офис|оф\.)\s*[\w/-]+', '', addr, flags=re.IGNORECASE)
    addr = re.sub(r',?\s*(этаж|эт\.)\s*[\w/-]+', '', addr, flags=re.IGNORECASE)
    # убрать БЦ "Название"
    addr = re.sub(r',?\s*БЦ\s*[«""][^»""]+[»""]', '', addr, flags=re.IGNORECASE)
    # убрать "корп. N", "стр. N", "к. N"
    addr = re.sub(r',?\s*(корп\.|стр\.|к\.)\s*[\w\d]+', '', addr, flags=re.IGNORECASE)
    # убрать "д. " перед номером дома
    addr = re.sub(r'\bд\.\s*(\d)', r'\1', addr)

    # раскрыть сокращения типов улиц
    replacements = [
        (r'\bпр-т\b', 'проспект'), (r'\bпр-кт\b', 'проспект'),
        (r'\bпр\.(?=[\s,]|$)', 'проспект'),
        (r'\bпр-д\b', 'проезд'),
        (r'\bб-р\b', 'бульвар'),   (r'\bбул\.\b', 'бульвар'),
        (r'\bш\.(?=[\s,]|$)', 'шоссе'),
        (r'\bул\.(?=[\s,]|$)', 'улица'),
        (r'\bпл\.(?=[\s,]|$)', 'площадь'),
        (r'\bнаб\.(?=[\s,]|$)', 'набережная'),
        (r'\bпер\.(?=[\s,]|$)', 'переулок'),
    ]
    for pattern, repl in replacements:
        addr = re.sub(pattern, repl, addr, flags=re.IGNORECASE)

    # почистить двойные запятые/пробелы
    addr = re.sub(r',\s*,', ',', addr)
    addr = re.sub(r'\s+', ' ', addr).strip().strip(',').strip()
    return addr


def _geocode(query):
    url = (
        "https://nominatim.openstreetmap.org/search?q="
        + urllib.parse.quote(query)
        + "&format=json&limit=1&accept-language=ru"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "HRRating/1.0"})
    with urllib.request.urlopen(req, timeout=10, context=_SSL_CTX) as resp:
        data = json.loads(resp.read())
    return data


class Command(BaseCommand):
    help = "Геокодирует адреса агентств и сохраняет координаты (map_lat, map_lon)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--overwrite', action='store_true',
            help='Перезаписать уже заполненные координаты'
        )

    def handle(self, *args, **options):
        qs = Agency.objects.all()
        if not options['overwrite']:
            qs = qs.filter(map_lat__isnull=True)

        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS("Все координаты уже заполнены."))
            return

        self.stdout.write(f"Геокодирование {total} агентств…")
        ok = fail = skip = 0

        for agency in qs:
            if not agency.address:
                skip += 1
                self.stdout.write(f"  [пропуск] {agency.name} — нет адреса")
                continue

            cleaned = _clean_address(agency.address)
            # попытка 1: город + очищенный адрес
            # попытка 2: только город + улица + дом (первые 2 части адреса)
            queries = [
                f"{agency.city}, {cleaned}",
                f"{agency.city}, " + ", ".join(cleaned.split(",")[:2]),
            ]

            data = None
            for q in queries:
                try:
                    data = _geocode(q)
                    time.sleep(1.1)
                    if data:
                        break
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  ✗ {agency.name}: ошибка — {e}"))
                    time.sleep(1.1)
                    break

            if data:
                agency.map_lat = float(data[0]["lat"])
                agency.map_lon = float(data[0]["lon"])
                agency.save(update_fields=["map_lat", "map_lon"])
                ok += 1
                self.stdout.write(f"  ✓ {agency.name}: {agency.map_lat:.5f}, {agency.map_lon:.5f}")
            else:
                fail += 1
                self.stdout.write(self.style.WARNING(f"  ✗ {agency.name}: не найден — «{queries[0]}»"))

        self.stdout.write(self.style.SUCCESS(
            f"\nГотово. Найдено: {ok}, не найдено: {fail}, пропущено (нет адреса): {skip}"
        ))
