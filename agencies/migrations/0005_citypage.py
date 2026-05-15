from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0004_faqitem_methodologyblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Город (отображаемое)')),
                ('city_filter', models.CharField(max_length=100, verbose_name='Фильтр по Agency.city')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug (часть URL)')),
                ('is_published', models.BooleanField(default=False, verbose_name='Опубликована')),
                ('meta_title', models.CharField(default='Рейтинг HR агентств 2026', max_length=200, verbose_name='Meta Title')),
                ('meta_description', models.TextField(blank=True, verbose_name='Meta Description')),
                ('meta_keywords', models.CharField(blank=True, max_length=500, verbose_name='Meta Keywords')),
                ('h1', models.CharField(default='Лучшие HR‑агентства — без рекламы и накруток', max_length=300, verbose_name='Заголовок H1')),
                ('hero_subtitle', models.TextField(blank=True, verbose_name='Подзаголовок (герой)')),
                ('seo_title', models.CharField(default='Как мы составляем независимый рейтинг', max_length=300, verbose_name='Заголовок секции «Методология»')),
                ('seo_lead', models.TextField(blank=True, verbose_name='Вводный текст методологии')),
            ],
            options={
                'verbose_name': 'Страница города',
                'verbose_name_plural': 'Страницы городов',
                'ordering': ['name'],
            },
        ),
    ]
