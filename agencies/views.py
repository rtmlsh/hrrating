import urllib.request
import urllib.parse
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.conf import settings
from .models import Agency, Category, SiteSettings, CityLink, FeedbackMessage, FaqItem, MethodologyBlock, CityPage, ResumeConstructorFaq, ResumeConstructorPage


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


def resume_constructor(request):
    db_faq = list(ResumeConstructorFaq.objects.filter(is_active=True))
    if db_faq:
        faq_static = [(item.question, item.answer) for item in db_faq]
    else:
        faq_static = [
            ("Нужна ли регистрация для создания резюме?",
             "Нет, регистрация не нужна. Создайте и скачайте резюме полностью бесплатно и без создания аккаунта."),
            ("Это бесплатно?",
             "Да, конструктор полностью бесплатный. Скачивание PDF также бесплатно без каких-либо ограничений."),
            ("Можно ли создать резюме на телефоне?",
             "Да, конструктор адаптирован для мобильных устройств и работает в браузере смартфона без установки приложений."),
            ("Сохраняются ли мои данные?",
             "Данные автоматически сохраняются в браузере (localStorage). Если закроете вкладку и вернётесь — всё восстановится."),
            ("Какой формат скачивать: PDF или Word?",
             "Для отправки работодателю рекомендуем PDF — он выглядит одинаково на любом устройстве и не поддаётся случайному редактированию."),
            ("Нужно ли добавлять фото в резюме?",
             "Фото уместно в большинстве российских компаний. Используйте деловую фотографию на нейтральном фоне."),
            ("Чем CV отличается от резюме?",
             "Резюме — краткий документ на 1–2 страницы для российского рынка. CV (Curriculum Vitae) — подробный документ, принятый в международных и академических организациях."),
            ("Можно ли создать резюме без опыта работы?",
             "Да. Укажите учебные проекты, стажировки, волонтёрство и навыки. Добавьте раздел «О себе» с описанием ваших сильных сторон."),
            ("Как сохранить резюме в формате PDF?",
             "Нажмите кнопку «Скачать PDF» — браузер откроет диалог печати. Выберите «Сохранить как PDF» в качестве принтера и нажмите «Сохранить»."),
            ("Сколько страниц должно быть резюме?",
             "Оптимально — 1 страница. Для кандидатов с опытом от 5 лет допустимо 2 страницы. Рекрутер просматривает резюме 6–10 секунд — не перегружайте его."),
        ]
    page = ResumeConstructorPage.get()
    return render(request, "agencies/resume_constructor.html", {"faq_static": faq_static, "page": page})


def _count_label(count):
    if count == 1:
        return "1 агентство"
    if count in (2, 3, 4):
        return f"{count} агентства"
    return f"{count} агентств"


def city_index(request, slug):
    # Сначала проверяем — не московское ли агентство это
    moscow_agency = Agency.objects.filter(slug=slug, city="Москва").first()
    if moscow_agency:
        form_errors, captcha_error = {}, False
        if request.method == "POST":
            form_errors, saved, captcha_error = _handle_review_post(request, moscow_agency)
            if saved:
                return redirect(request.path + "?review=sent#reviews")
        ctx = _agency_detail_ctx(moscow_agency, None, "", request.GET.get("rsort", "new"))
        ctx.update({
            "form_errors": form_errors,
            "review_sent": request.GET.get("review") == "sent",
            "review_captcha_error": captcha_error,
            "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
        })
        return render(request, "agencies/agency_detail.html", ctx)

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


def _agency_detail_ctx(agency, city_page, city_slug, review_sort="new"):
    from django.db.models import Avg as _Avg, Count as _Count
    sort_map = {
        "new":  "-created_at",
        "old":  "created_at",
        "high": "-rating",
        "low":  "rating",
    }
    reviews = agency.reviews.filter(is_approved=True).order_by(sort_map.get(review_sort, "-created_at"))
    rating = round(agency.avg_rating, 1) if agency.avg_rating else 0.0

    criteria = [
        ("Качество кандидатов", agency.criteria_quality),
        ("Скорость закрытия", agency.criteria_speed),
        ("Цена/качество", agency.criteria_price),
        ("Поддержка клиентов", agency.criteria_support),
    ]

    ext_ratings = []
    for key, label, r_field, c_field, u_field in [
        ("yandex", "Яндекс.Карты", "ext_yandex_rating", "ext_yandex_count", "ext_yandex_url"),
        ("google", "Google Maps", "ext_google_rating", "ext_google_count", "ext_google_url"),
        ("2gis", "2ГИС", "ext_2gis_rating", "ext_2gis_count", "ext_2gis_url"),
    ]:
        r = getattr(agency, r_field)
        if r:
            ext_ratings.append({
                "key": key, "label": label,
                "rating": round(r, 1),
                "count": getattr(agency, c_field),
                "url": getattr(agency, u_field),
            })

    source_agg = (
        reviews.values("source")
        .annotate(cnt=_Count("id"), avg=_Avg("rating"))
        .order_by("source")
    )
    SOURCE_LABELS = dict(agency.reviews.model.SOURCE_CHOICES)
    review_sources = [
        {"key": s["source"], "label": SOURCE_LABELS.get(s["source"], s["source"]),
         "count": s["cnt"], "avg": round(s["avg"] or 0, 1)}
        for s in source_agg if s["cnt"] > 0
    ]

    # Предложный падеж города
    CITY_PREP = {
        "Москва": "Москве", "Санкт-Петербург": "Санкт-Петербурге",
        "Екатеринбург": "Екатеринбурге", "Новосибирск": "Новосибирске",
        "Казань": "Казани", "Уфа": "Уфе", "Самара": "Самаре",
        "Краснодар": "Краснодаре", "Ростов-на-Дону": "Ростове-на-Дону",
        "Воронеж": "Воронеже", "Челябинск": "Челябинске",
        "Красноярск": "Красноярске", "Нижний Новгород": "Нижнем Новгороде",
        "Пермь": "Перми", "Омск": "Омске", "Волгоград": "Волгограде",
        "Тюмень": "Тюмени", "Уфа": "Уфе", "Иркутск": "Иркутске",
        "Хабаровск": "Хабаровске", "Владивосток": "Владивостоке",
        "Ярославль": "Ярославле", "Томск": "Томске", "Барнаул": "Барнауле",
    }
    city_prep = CITY_PREP.get(agency.city, agency.city)

    # Похожие агентства: та же категория или тот же город, не текущее
    cat_ids = list(agency.categories.values_list("id", flat=True))
    similar_qs = (
        Agency.objects
        .exclude(pk=agency.pk)
        .filter(city=agency.city)
        .prefetch_related("categories")
        .annotate(annotated_rating=_Avg("reviews__rating"))
        .order_by("-annotated_rating")
    )
    if cat_ids:
        similar_qs = similar_qs.filter(categories__id__in=cat_ids).distinct()
    similar_agencies = [
        {"obj": a, "rating": round(a.annotated_rating or 0, 1)}
        for a in similar_qs[:4]
    ]

    return {
        "agency": agency,
        "city_slug": city_slug,
        "city_page": city_page,
        "rating": rating,
        "reviews": reviews,
        "review_sources": review_sources,
        "criteria": criteria,
        "specializations": agency.get_specializations_list(),
        "external_ratings": ext_ratings,
        "platform_ratings": [{"key": s["key"], "label": s["label"], "avg": s["avg"], "count": s["count"]} for s in review_sources],
        "same_as_urls": [u for u in [agency.ext_yandex_url, agency.ext_google_url, agency.ext_2gis_url, agency.website] if u],
        "review_sort": review_sort,
        "similar_agencies": similar_agencies,
        "city_prep": city_prep,
    }


def _handle_review_post(request, agency):
    """Обрабатывает POST с формой отзыва. Возвращает (errors, saved, captcha_error)."""
    errors = {}
    author = request.POST.get("author", "").strip()
    text   = request.POST.get("text", "").strip()
    rating = request.POST.get("rating", "").strip()
    token  = request.POST.get("g-recaptcha-response", "")

    if not author:
        errors["author"] = "Укажите имя"
    elif len(author) > 150:
        errors["author"] = "Не более 150 символов"

    if not text:
        errors["text"] = "Напишите текст отзыва"
    elif len(text) > 2000:
        errors["text"] = "Не более 2000 символов"

    if not rating or not rating.isdigit() or int(rating) not in range(1, 6):
        errors["rating"] = "Выберите оценку от 1 до 5"

    if errors:
        return errors, False, False

    if not _verify_recaptcha(token):
        return errors, False, True

    from agencies.models import Review as R
    R.objects.create(agency=agency, author=author, text=text,
                     rating=int(rating), source="other")
    return errors, True, False


def agency_detail(request, city_slug, agency_slug):
    """Детальная страница агентства не-московских городов: /<city_slug>/<agency_slug>/"""
    city_page = get_object_or_404(CityPage, slug=city_slug, is_published=True)
    agency = get_object_or_404(Agency, slug=agency_slug, city=city_page.city_filter)

    form_errors, captcha_error = {}, False
    if request.method == "POST":
        form_errors, saved, captcha_error = _handle_review_post(request, agency)
        if saved:
            return redirect(request.path + "?review=sent#reviews")

    ctx = _agency_detail_ctx(agency, city_page, city_slug, request.GET.get("rsort", "new"))
    ctx.update({
        "form_errors": form_errors,
        "review_sent": request.GET.get("review") == "sent",
        "review_captcha_error": captcha_error,
        "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
    })
    return render(request, "agencies/agency_detail.html", ctx)


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