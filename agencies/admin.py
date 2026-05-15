from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from django.utils.html import format_html
from django import forms
from .models import Agency, Category, SiteSettings, CityLink, FeedbackMessage, FaqItem, MethodologyBlock, CityPage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = [
        "name", "city", "display_avg_rating",
        "speed_score", "founded_year",
    ]
    list_filter = ["categories", "city"]
    search_fields = ["name", "description", "address"]
    filter_horizontal = ["categories"]
    fieldsets = (
        (None, {"fields": ("name", "description", "city", "address", "phone", "website", "founded_year", "categories")}),
        ("Специализации", {"fields": ("specializations",)}),
        ("Детальные критерии", {"fields": ("criteria_quality", "criteria_speed", "criteria_price", "criteria_support", "speed_score")}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        cities = ["Москва"] + list(
            CityPage.objects.order_by("name").values_list("city_filter", flat=True)
        )
        form.base_fields["city"].widget = forms.Select(
            choices=[(c, c) for c in cities],
            attrs={"class": "vTextField"},
        )
        return form

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        if "city" in request.GET:
            initial["city"] = request.GET["city"]
        return initial

    @admin.display(description="Рейтинг")
    def display_avg_rating(self, obj):
        return obj.avg_rating



@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("SEO / Мета-теги", {
            "fields": ("meta_title", "meta_description", "meta_keywords"),
            "description": "Заполните мета-теги для поисковой оптимизации страницы.",
        }),
        ("Контент страницы", {
            "fields": ("h1", "hero_subtitle", "agencies_heading"),
            "description": "H1 поддерживает HTML-теги (например, &lt;em&gt; для выделения цветом).",
        }),
        ("Карточки статистики (хедер)", {
            "fields": (
                ("stat1_value", "stat1_label"),
                ("stat2_value", "stat2_label"),
                ("stat3_value", "stat3_label"),
                ("stat4_value", "stat4_label"),
            ),
            "description": "Подпись: перенос строки через \\n — например «проверенных\\nагентств».",
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Редирект сразу на форму редактирования единственного объекта
        obj = SiteSettings.get()
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        return HttpResponseRedirect(
            reverse("admin:agencies_sitesettings_change", args=[obj.pk])
        )


@admin.register(CityLink)
class CityLinkAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "is_active", "sort_order"]
    list_editable = ["is_active", "sort_order"]
    list_display_links = ["name"]
    search_fields = ["name", "url"]
    fieldsets = (
        (None, {
            "fields": ("name", "url", "is_active", "sort_order"),
            "description": "Ссылки на рейтинги других городов отображаются в футере сайта.",
        }),
    )


@admin.register(FeedbackMessage)
class FeedbackMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "created_at", "is_read"]
    list_filter = ["is_read"]
    list_editable = ["is_read"]
    list_display_links = ["name"]
    search_fields = ["name", "email", "subject", "message"]
    readonly_fields = ["name", "email", "subject", "message", "created_at"]
    fieldsets = (
        (None, {
            "fields": ("name", "email", "subject", "message", "created_at", "is_read"),
        }),
    )


@admin.register(FaqItem)
class FaqItemAdmin(admin.ModelAdmin):
    list_display = ["question", "city_page", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]
    list_display_links = ["question"]
    list_filter = ["city_page", "is_active"]
    fieldsets = (
        (None, {
            "fields": ("city_page", "question", "answer", "sort_order", "is_active"),
            "description": "Поле «Страница города» оставьте пустым для глобального FAQ (отображается на всех городах без собственных записей).",
        }),
    )


@admin.register(MethodologyBlock)
class MethodologyBlockAdmin(admin.ModelAdmin):
    list_display = ["title", "city_page", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]
    list_display_links = ["title"]
    list_filter = ["city_page", "is_active"]
    fieldsets = (
        (None, {
            "fields": ("city_page", "title", "text", "icon_svg", "sort_order", "is_active"),
            "description": "Поле «Страница города» оставьте пустым для глобального блока. Текст поддерживает &lt;strong&gt;. SVG-иконка — полный тег &lt;svg …&gt;…&lt;/svg&gt;.",
        }),
    )


class FaqItemInline(admin.StackedInline):
    model = FaqItem
    extra = 0
    fields = ["question", "answer", "sort_order", "is_active"]
    verbose_name = "Вопрос FAQ"
    verbose_name_plural = "FAQ (для этого города)"
    show_change_link = True


class MethodologyBlockInline(admin.StackedInline):
    model = MethodologyBlock
    extra = 0
    fields = ["title", "text", "icon_svg", "sort_order", "is_active"]
    verbose_name = "Блок методологии"
    verbose_name_plural = "Методология (для этого города)"
    show_change_link = True


@admin.register(CityPage)
class CityPageAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_published", "city_filter", "agency_count"]
    list_editable = ["is_published"]
    list_display_links = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["agency_link", "copy_global_button"]
    inlines = [MethodologyBlockInline, FaqItemInline]
    fieldsets = (
        ("Основное", {
            "fields": ("name", "city_filter", "slug", "is_published", "agency_link"),
            "description": "«Фильтр по Agency.city» — точное значение поля «Город» у агентств, которые попадут на эту страницу.",
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description", "meta_keywords"),
        }),
        ("Контент страницы", {
            "fields": ("h1", "hero_subtitle", "agencies_heading", "seo_title", "seo_lead"),
            "description": "H1 поддерживает HTML-теги (например, &lt;em&gt; для выделения цветом).",
        }),
        ("Карточки статистики (хедер)", {
            "fields": (
                ("stat1_value", "stat1_label"),
                ("stat2_value", "stat2_label"),
                ("stat3_value", "stat3_label"),
                ("stat4_value", "stat4_label"),
            ),
            "description": "Перенос строки в подписи через \\n — например «проверенных\\nагентств».",
        }),
        ("Контент блоков", {
            "fields": ("copy_global_button",),
            "description": (
                "Блоки «Методология» и «FAQ» ниже переопределяют глобальные для этого города. "
                "Если город-блоков нет — сайт показывает глобальные автоматически."
            ),
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "<int:pk>/copy-global/",
                self.admin_site.admin_view(self.copy_global_view),
                name="agencies_citypage_copy_global",
            ),
        ]
        return custom + urls

    def copy_global_view(self, request, pk):
        city_page = CityPage.objects.get(pk=pk)

        meth_global = MethodologyBlock.objects.filter(city_page=None, is_active=True)
        faq_global = FaqItem.objects.filter(city_page=None, is_active=True)

        meth_copied = faq_copied = 0

        if not MethodologyBlock.objects.filter(city_page=city_page).exists():
            for b in meth_global:
                MethodologyBlock.objects.create(
                    city_page=city_page,
                    icon_svg=b.icon_svg,
                    title=b.title,
                    text=b.text,
                    sort_order=b.sort_order,
                    is_active=b.is_active,
                )
                meth_copied += 1

        if not FaqItem.objects.filter(city_page=city_page).exists():
            for f in faq_global:
                FaqItem.objects.create(
                    city_page=city_page,
                    question=f.question,
                    answer=f.answer,
                    sort_order=f.sort_order,
                    is_active=f.is_active,
                )
                faq_copied += 1

        if meth_copied or faq_copied:
            self.message_user(
                request,
                f"Скопировано: {meth_copied} блоков методологии, {faq_copied} вопросов FAQ. Теперь редактируйте их ниже.",
                messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                "Блоки уже существуют для этого города — копирование пропущено.",
                messages.WARNING,
            )

        return HttpResponseRedirect(
            reverse("admin:agencies_citypage_change", args=[pk])
        )

    @admin.display(description="Скопировать глобальные блоки")
    def copy_global_button(self, obj):
        if not obj.pk:
            return "Сначала сохраните страницу города."
        has_meth = MethodologyBlock.objects.filter(city_page=obj).exists()
        has_faq = FaqItem.objects.filter(city_page=obj).exists()
        if has_meth and has_faq:
            return format_html(
                '<span style="color:#6b7280">Городские блоки уже заданы — редактируйте инлайны ниже.</span>'
            )
        url = reverse("admin:agencies_citypage_copy_global", args=[obj.pk])
        return format_html(
            '<a href="{}" class="button" style="background:#0066ff;color:#fff;padding:8px 18px;'
            'border-radius:6px;text-decoration:none;font-weight:600;font-size:13px;">'
            '⬇ Скопировать из глобальных</a>'
            '<p style="margin-top:6px;color:#6b7280;font-size:12px">'
            'Копирует глобальные блоки методологии и FAQ в этот город. '
            'Срабатывает только если блоки ещё не заданы.</p>',
            url,
        )

    @admin.display(description="Агентств")
    def agency_count(self, obj):
        return Agency.objects.filter(city=obj.city_filter).count()

    @admin.display(description="Агентства города")
    def agency_link(self, obj):
        if not obj.pk:
            return "—"
        count = Agency.objects.filter(city=obj.city_filter).count()
        list_url = reverse("admin:agencies_agency_changelist") + f"?city={obj.city_filter}"
        add_url = reverse("admin:agencies_agency_add") + f"?city={obj.city_filter}"
        return format_html(
            '<a href="{}">{} агентств(а) в списке</a>&nbsp;&nbsp;·&nbsp;&nbsp;'
            '<a href="{}" style="font-weight:600;">＋ Добавить агентство</a>',
            list_url, count, add_url,
        )