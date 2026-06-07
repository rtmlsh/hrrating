from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("feedback/", views.feedback, name="feedback"),
    path("konstruktor-rezume/", views.resume_constructor, name="resume_constructor"),
    path("kalkulyator-zarplaty/", views.salary_calculator, name="salary_calculator"),
    path("api/salary/", views.salary_api, name="salary_api"),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),
    path("<slug:city_slug>/<slug:agency_slug>/", views.agency_detail, name="agency_detail"),
    path("<slug:slug>/", views.city_index, name="city_index"),
]
