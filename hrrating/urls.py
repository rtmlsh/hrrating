from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView
from agencies.sitemaps import StaticSitemap, CityPageSitemap

sitemaps = {
    "static": StaticSitemap,
    "cities": CityPageSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico", permanent=True)),
    path("", include("agencies.urls")),
]
