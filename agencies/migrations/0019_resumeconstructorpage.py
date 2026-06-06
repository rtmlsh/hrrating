from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0018_resumeconstructorfaq'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResumeConstructorPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_title', models.CharField(default='Конструктор резюме онлайн — создать резюме бесплатно | HR Rating', max_length=200, verbose_name='Title')),
                ('meta_description', models.TextField(default='Конструктор резюме онлайн — создайте профессиональное резюме бесплатно за 5 минут. Без регистрации, скачать PDF, 4 шаблона.', verbose_name='Meta Description')),
                ('og_title', models.CharField(blank=True, default='Конструктор резюме онлайн — бесплатно | HR Rating', max_length=200, verbose_name='OG Title')),
                ('og_description', models.TextField(blank=True, default='Создайте резюме за 5 минут. Бесплатно, без регистрации, скачать PDF.', verbose_name='OG Description')),
            ],
            options={
                'verbose_name': 'Настройки страницы конструктора',
                'verbose_name_plural': 'Настройки страницы конструктора',
            },
        ),
    ]
