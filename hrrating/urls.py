from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from agencies.sitemaps import StaticSitemap, CityPageSitemap

sitemaps = {
    "static": StaticSitemap,
    "cities": CityPageSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("", include("agencies.urls")),
]
