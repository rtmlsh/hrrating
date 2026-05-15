from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("Slug", unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Agency(models.Model):
    name = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")
    city = models.CharField("Город", max_length=100, default="Москва")
    address = models.CharField("Адрес", max_length=300, blank=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    founded_year = models.PositiveSmallIntegerField("Год основания", null=True, blank=True)
    website = models.URLField("Сайт", blank=True)
    is_verified = models.BooleanField("Верифицировано", default=False)
    categories = models.ManyToManyField(Category, verbose_name="Категории", blank=True)
    specializations = models.TextField(
        "Специализации",
        blank=True,
        help_text="Список специализаций через запятую",
    )
    criteria_quality = models.FloatField("Качество кандидатов", default=0)
    criteria_speed = models.FloatField("Скорость закрытия", default=0)
    criteria_price = models.FloatField("Цена", default=0)
    criteria_support = models.FloatField("Поддержка", default=0)
    speed_score = models.FloatField("Скорость (0–10)", default=0)
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    class Meta:
        verbose_name = "Агентство"
        verbose_name_plural = "Агентства"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def avg_rating(self):
        result = self.reviews.aggregate(avg=Avg("rating"))["avg"]
        return round(result, 2) if result else 0.0

    @property
    def review_count(self):
        return self.reviews.count()

    def get_specializations_list(self):
        return [s.strip() for s in self.specializations.split(",") if s.strip()]

    @property
    def years_on_market(self):
        from datetime import date
        if self.founded_year:
            return date.today().year - self.founded_year
        return None

    @property
    def years_label(self):
        n = self.years_on_market
        if not n:
            return ""
        if 11 <= n % 100 <= 14:
            return f"{n} лет"
        r = n % 10
        if r == 1:
            return f"{n} год"
        if 2 <= r <= 4:
            return f"{n} года"
        return f"{n} лет"


class SiteSettings(models.Model):
    meta_title = models.CharField(
        "Meta Title", max_length=200,
        default="Рейтинг HR агентств Москвы 2026",
    )
    meta_description = models.TextField(
        "Meta Description",
        default="Независимый рейтинг кадровых агентств Москвы по качеству подбора и скорости закрытия вакансий.",
    )
    meta_keywords = models.CharField(
        "Meta Keywords", max_length=500, blank=True,
        default="HR агентства Москва, кадровые агентства, рейтинг рекрутинг 2026",
    )
    h1 = models.CharField(
        "Заголовок H1", max_length=300,
        default="Лучшие HR&#8209;агентства <em>Москвы</em> — без рекламы и накруток",
    )
    hero_subtitle = models.TextField(
        "Подзаголовок (герой)", blank=True,
        default="Мы оцениваем кадровые агентства по качеству подбора, скорости закрытия вакансий и отзывам реальных работодателей. Без платных позиций.",
    )
    stat1_value = models.CharField("Стат 1 — число", max_length=20, default="100+")
    stat1_label = models.CharField("Стат 1 — подпись", max_length=60, default="проверенных\nагентств")
    stat2_value = models.CharField("Стат 2 — число", max_length=20, default="4")
    stat2_label = models.CharField("Стат 2 — подпись", max_length=60, default="критерия\nоценки")
    stat3_value = models.CharField("Стат 3 — число", max_length=20, default="12")
    stat3_label = models.CharField("Стат 3 — подпись", max_length=60, default="месяцев\nисследования")
    stat4_value = models.CharField("Стат 4 — число", max_length=20, default="0₽")
    stat4_label = models.CharField("Стат 4 — подпись", max_length=60, default="платных\nразмещений")
    agencies_heading = models.CharField(
        "Заголовок раздела «Агентства …»", max_length=200,
        default="Агентства Москвы",
        help_text="Например: «Агентства Москвы» или «Лучшие кадровые агентства»",
    )

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # singleton — нельзя удалить

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class CityLink(models.Model):
    name = models.CharField("Город", max_length=100)
    url = models.CharField(
        "URL", max_length=300,
        help_text="Например: /spb/ или https://example.com/hr-rating-spb/",
    )
    is_active = models.BooleanField("Активна", default=True)
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Город (перелинковка)"
        verbose_name_plural = "Города (перелинковка)"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class CityPage(models.Model):
    name = models.CharField("Город (отображаемое)", max_length=100,
        help_text="Например: Санкт-Петербург")
    name_genitive = models.CharField("Город (родительный падеж)", max_length=100,
        help_text="Например: Санкт-Петербурга — используется в заголовке «Агентства …»")
    city_filter = models.CharField("Фильтр по Agency.city", max_length=100,
        help_text="Точное значение поля «Город» у агентств — например: Санкт-Петербург")
    slug = models.SlugField("Slug (часть URL)", unique=True,
        help_text="Например: spb → страница будет на /spb/")
    is_published = models.BooleanField("Опубликована", default=False)

    meta_title = models.CharField("Meta Title", max_length=200,
        default="Рейтинг HR агентств 2026")
    meta_description = models.TextField("Meta Description", blank=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=500, blank=True)
    h1 = models.CharField("Заголовок H1", max_length=300,
        default="Лучшие HR&#8209;агентства — без рекламы и накруток",
        help_text="Поддерживает HTML-теги, например &lt;em&gt;")
    hero_subtitle = models.TextField("Подзаголовок (герой)", blank=True)
    agencies_heading = models.CharField(
        "Заголовок раздела «Агентства …»", max_length=200,
        blank=True,
        help_text="Например: «Агентства Санкт-Петербурга». Если пусто — подставится «Агентства {город}».",
    )
    seo_title = models.CharField("Заголовок секции «Методология»", max_length=300,
        default="Как мы составляем независимый рейтинг")
    seo_lead = models.TextField("Вводный текст методологии", blank=True)
    stat1_value = models.CharField("Стат 1 — число", max_length=20, default="100+")
    stat1_label = models.CharField("Стат 1 — подпись", max_length=60, default="проверенных\nагентств")
    stat2_value = models.CharField("Стат 2 — число", max_length=20, default="4")
    stat2_label = models.CharField("Стат 2 — подпись", max_length=60, default="критерия\nоценки")
    stat3_value = models.CharField("Стат 3 — число", max_length=20, default="12")
    stat3_label = models.CharField("Стат 3 — подпись", max_length=60, default="месяцев\nисследования")
    stat4_value = models.CharField("Стат 4 — число", max_length=20, default="0₽")
    stat4_label = models.CharField("Стат 4 — подпись", max_length=60, default="платных\nразмещений")

    class Meta:
        verbose_name = "Страница города"
        verbose_name_plural = "Страницы городов"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.slug}/"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        CityLink.objects.filter(name=self.name).update(url=self.get_absolute_url())
        if is_new:
            self._copy_global_blocks()

    def _copy_global_blocks(self):
        for b in MethodologyBlock.objects.filter(city_page=None):
            MethodologyBlock.objects.create(
                city_page=self,
                icon_svg=b.icon_svg,
                title=b.title,
                text=b.text,
                sort_order=b.sort_order,
                is_active=b.is_active,
            )
        for f in FaqItem.objects.filter(city_page=None):
            FaqItem.objects.create(
                city_page=self,
                question=f.question,
                answer=f.answer,
                sort_order=f.sort_order,
                is_active=f.is_active,
            )


class FaqItem(models.Model):
    city_page = models.ForeignKey(
        "CityPage",
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="faq_items",
        verbose_name="Страница города",
        help_text="Оставьте пустым — будет глобальным (для всех городов без своих FAQ).",
    )
    question = models.CharField("Вопрос", max_length=300)
    answer = models.TextField("Ответ")
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Вопрос FAQ"
        verbose_name_plural = "FAQ"
        ordering = ["sort_order"]

    def __str__(self):
        prefix = f"[{self.city_page.name}] " if self.city_page_id else ""
        return f"{prefix}{self.question}"


class MethodologyBlock(models.Model):
    city_page = models.ForeignKey(
        "CityPage",
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="methodology_blocks",
        verbose_name="Страница города",
        help_text="Оставьте пустым — будет глобальным (для всех городов без своих блоков).",
    )
    icon_svg = models.TextField(
        "SVG-иконка", blank=True,
        help_text="Полный тег &lt;svg …&gt;…&lt;/svg&gt;",
    )
    title = models.CharField("Заголовок", max_length=200)
    text = models.TextField("Текст (поддерживает &lt;strong&gt;)")
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Блок методологии"
        verbose_name_plural = "Методология"
        ordering = ["sort_order"]

    def __str__(self):
        prefix = f"[{self.city_page.name}] " if self.city_page_id else ""
        return f"{prefix}{self.title}"


class FeedbackMessage(models.Model):
    name = models.CharField("Имя", max_length=150)
    email = models.EmailField("Email")
    subject = models.CharField("Тема", max_length=200, blank=True)
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField("Дата", auto_now_add=True)
    is_read = models.BooleanField("Прочитано", default=False)

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}> — {self.created_at:%d.%m.%Y}"


class Review(models.Model):
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Агентство",
    )
    rating = models.PositiveSmallIntegerField(
        "Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField("Текст отзыва", blank=True)
    author = models.CharField("Автор", max_length=150, blank=True)
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.agency.name} — {self.rating}★"