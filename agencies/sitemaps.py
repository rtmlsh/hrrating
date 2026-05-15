from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import CityPage


class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return ["index", "feedback", "privacy", "terms"]

    def location(self, item):
        return reverse(item)


class CityPageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return CityPage.objects.filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return None
