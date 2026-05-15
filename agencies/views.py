import urllib.request
import urllib.parse
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.conf import settings
from .models import Agency, Category, SiteSettings, CityLink, FeedbackMessage, FaqItem, MethodologyBlock, CityPage


def _verify_recaptcha(token, min_score=0.5):
    if not settings.RECAPTCHA_SECRET_KEY or not token:
        return True
    data = urllib.parse.urlencode({
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': token,
    }).encode()
    try:
        with urllib.request.urlopen('https://www.google.com/recaptcha/api/siteverify', data, timeout=5) as resp:
            result = json.loads(resp.read())
        return result.get('success') and result.get('score', 0) >= min_score
    except Exception:
        return True


def index(request):
    categories = Category.objects.all()
    category_slug = request.GET.get("spec", "all")
    search = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "rating")

    qs = (
        Agency.objects
        .filter(city="Москва")
        .prefetch_related("categories")
        .annotate(annotated_rating=Avg("reviews__rating"))
    )

    if category_slug and category_slug != "all":
        qs = qs.filter(categories__slug=category_slug)

    if search:
        qs = qs.filter(
            name__icontains=search
        ) | qs.filter(
            specializations__icontains=search
        )

    agency_list = _build_agency_list(qs, sort)

    ctx = {
        "agency_list": agency_list,
        "categories": categories,
        "current_spec": category_slug,
        "search": search,
        "sort": sort,
        "count_label": _count_label(len(agency_list)),
        "site": SiteSettings.get(),
        "city_links": CityLink.objects.filter(is_active=True),
        "faq_items": FaqItem.objects.filter(is_active=True, city_page=None),
        "methodology_blocks": MethodologyBlock.objects.filter(is_active=True, city_page=None),
    }
    if request.GET.get("partial") == "1":
        return render(request, "agencies/_agency_results.html", ctx)
    return render(request, "agencies/index.html", ctx)


def _build_agency_list(qs, sort):
    sort_map = {"rating": "-annotated_rating", "speed": "-speed_score", "name": "name"}
    qs = qs.order_by(sort_map.get(sort, "-annotated_rating"))
    result = []
    for rank, a in enumerate(qs, start=1):
        result.append({
            "obj": a,
            "rank": rank,
            "rating": round(a.annotated_rating or 0, 2),
            "specializations": a.get_specializations_list(),
        })
    return result


def _count_label(count):
    if count == 1:
        return "1 агентство"
    if count in (2, 3, 4):
        return f"{count} агентства"
    return f"{count} агентств"


def city_index(request, slug):
    city_page = get_object_or_404(CityPage, slug=slug, is_published=True)
    categories = Category.objects.all()
    category_slug = request.GET.get("spec", "all")
    search = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "rating")

    qs = (
        Agency.objects
        .filter(city=city_page.city_filter)
        .prefetch_related("categories")
        .annotate(annotated_rating=Avg("reviews__rating"))
    )
    if category_slug and category_slug != "all":
        qs = qs.filter(categories__slug=category_slug)
    if search:
        qs = qs.filter(name__icontains=search) | qs.filter(specializations__icontains=search)

    agency_list = _build_agency_list(qs, sort)

    faq_items = FaqItem.objects.filter(is_active=True, city_page=city_page)
    if not faq_items.exists():
        faq_items = FaqItem.objects.filter(is_active=True, city_page=None)

    methodology_blocks = MethodologyBlock.objects.filter(is_active=True, city_page=city_page)
    if not methodology_blocks.exists():
        methodology_blocks = MethodologyBlock.objects.filter(is_active=True, city_page=None)

    ctx = {
        "agency_list": agency_list,
        "categories": categories,
        "current_spec": category_slug,
        "search": search,
        "sort": sort,
        "count_label": _count_label(len(agency_list)),
        "site": city_page,
        "city_links": CityLink.objects.filter(is_active=True),
        "faq_items": faq_items,
        "methodology_blocks": methodology_blocks,
        "city_page": city_page,
    }
    if request.GET.get("partial") == "1":
        return render(request, "agencies/_agency_results.html", ctx)
    return render(request, "agencies/index.html", ctx)


def terms(request):
    return render(request, "agencies/terms.html")


def privacy(request):
    return render(request, "agencies/privacy.html")


def feedback(request):
    recaptcha_error = False
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()
        token = request.POST.get("g-recaptcha-response", "")
        if name and email and message:
            if _verify_recaptcha(token):
                FeedbackMessage.objects.create(
                    name=name, email=email, subject=subject, message=message
                )
                return redirect("/feedback/?sent=1")
            else:
                recaptcha_error = True
    sent = request.GET.get("sent") == "1"
    return render(request, "agencies/feedback.html", {
        "sent": sent,
        "recaptcha_error": recaptcha_error,
        "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
    })