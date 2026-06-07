from datetime import date
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Agency, CityPage

FALLBACK_DATE = date(2026, 5, 16)

STATIC_PRIORITIES = {
    "index": 1.0,
    "salary_calculator": 0.9,
    "resume_constructor": 0.9,
    "feedback": 0.3,
    "privacy": 0.2,
    "terms": 0.2,
}


class StaticSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return ["index", "salary_calculator", "resume_constructor", "feedback", "privacy", "terms"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return STATIC_PRIORITIES.get(item, 0.5)

    def lastmod(self, item):
        return FALLBACK_DATE


class CityPageSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return CityPage.objects.filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        latest = Agency.objects.filter(city=obj.city_filter).order_by("-created_at").values_list("created_at", flat=True).first()
        if latest:
            return latest.date()
        return FALLBACK_DATE


class AgencySitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Agency.objects.filter(slug__isnull=False).exclude(slug="").order_by("city", "name")

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        latest_review = obj.reviews.order_by("-created_at").values_list("created_at", flat=True).first()
        if latest_review:
            return latest_review.date()
        return obj.created_at.date()
