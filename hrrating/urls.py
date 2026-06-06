from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView
from django.views.defaults import page_not_found
from agencies.sitemaps import StaticSitemap, CityPageSitemap, AgencySitemap

handler404 = page_not_found

sitemaps = {
    "static": StaticSitemap,
    "cities": CityPageSitemap,
    "agencies": AgencySitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico", permanent=True)),
    path("", include("agencies.urls")),
]
