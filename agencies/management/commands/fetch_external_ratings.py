"""
Обновить внешние рейтинги (Яндекс, Google, 2ГИС) для агентств.

  python manage.py fetch_external_ratings              # все агентства
  python manage.py fetch_external_ratings --id 1 2 3   # по ID
  python manage.py fetch_external_ratings --slug ancor # по slug
  python manage.py fetch_external_ratings --sources 2gis yandex  # выбрать платформы
"""

import time
from django.core.management.base import BaseCommand
from django.utils import timezone

from agencies.models import Agency
from agencies import parsers


SOURCE_FIELDS = {
    "yandex": ("ext_yandex_rating", "ext_yandex_count", "ext_yandex_url"),
    "google": ("ext_google_rating", "ext_google_count", "ext_google_url"),
    "2gis": ("ext_2gis_rating", "ext_2gis_count", "ext_2gis_url"),
}


class Command(BaseCommand):
    help = "Обновляет внешние рейтинги агентств с Яндекс.Карт, Google Maps и 2ГИС."

    def add_arguments(self, parser):
        parser.add_argument("--id", nargs="*", type=int, help="ID агентств")
        parser.add_argument("--slug", nargs="*", help="Slug-и агентств")
        parser.add_argument(
            "--sources", nargs="*",
            choices=list(SOURCE_FIELDS.keys()),
            default=list(SOURCE_FIELDS.keys()),
            help="Какие платформы обновить",
        )
        parser.add_argument("--delay", type=float, default=1.0,
            help="Пауза между запросами, сек (по умолчанию 1.0)")
        parser.add_argument("--force", action="store_true",
            help="Обновить даже если уже есть значение")

    def handle(self, *args, **opts):
        qs = Agency.objects.all()
        if opts.get("id"):
            qs = qs.filter(pk__in=opts["id"])
        if opts.get("slug"):
            qs = qs.filter(slug__in=opts["slug"])

        sources = opts["sources"]
        delay = opts["delay"]
        force = opts["force"]

        total = qs.count()
        if not total:
            self.stdout.write(self.style.WARNING("Нет агентств по заданным фильтрам."))
            return

        self.stdout.write(f"Обновляю {total} агентств(а) для платформ: {', '.join(sources)}\n")
        ok = 0
        for a in qs:
            self.stdout.write(f"\n→ #{a.pk} {a.name} ({a.city})")
            changed = False
            for src in sources:
                rating_f, count_f, url_f = SOURCE_FIELDS[src]
                if not force and getattr(a, rating_f) is not None:
                    self.stdout.write(f"  {src}: пропускаю (уже есть рейтинг)")
                    continue
                fn = parsers.PARSERS.get(src)
                if not fn:
                    continue
                try:
                    result = fn(a.name, a.city, a.address or "")
                except Exception as e:
                    self.stderr.write(f"  {src}: ошибка — {e}")
                    continue

                if not result:
                    self.stdout.write(f"  {src}: ничего не найдено")
                else:
                    rating = result.get("rating")
                    count = result.get("count")
                    url = result.get("url") or ""
                    if rating is not None:
                        setattr(a, rating_f, rating)
                    if count is not None:
                        setattr(a, count_f, count)
                    if url:
                        setattr(a, url_f, url)
                    changed = True
                    rs = f"{rating}" if rating is not None else "—"
                    cs = f"({count} отз.)" if count else ""
                    self.stdout.write(self.style.SUCCESS(f"  {src}: ★ {rs} {cs} {url}"))
                time.sleep(delay)

            if changed:
                a.ext_updated_at = timezone.now()
                a.save(update_fields=[
                    "ext_yandex_rating", "ext_yandex_count", "ext_yandex_url",
                    "ext_google_rating", "ext_google_count", "ext_google_url",
                    "ext_2gis_rating", "ext_2gis_count", "ext_2gis_url",
                    "ext_updated_at",
                ])
                ok += 1

        self.stdout.write(self.style.SUCCESS(f"\nГотово. Обновлено: {ok}/{total}"))
