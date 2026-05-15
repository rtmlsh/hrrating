from datetime import date
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import CityPage

LAST_UPDATED = date(2026, 5, 16)


class StaticSitemap(Sitemap):
    priority = 1.0

    def items(self):
        return ["index", "feedback", "privacy", "terms"]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return LAST_UPDATED


class CityPageSitemap(Sitemap):
    priority = 0.9

    def items(self):
        return CityPage.objects.filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return LAST_UPDATED
