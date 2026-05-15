from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0003_feedbackmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaqItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300, verbose_name='Вопрос')),
                ('answer', models.TextField(verbose_name='Ответ')),
                ('sort_order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Вопрос FAQ',
                'verbose_name_plural': 'FAQ',
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='MethodologyBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon_svg', models.TextField(blank=True, help_text='Полный тег <svg …>…</svg>', verbose_name='SVG-иконка')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст (поддерживает <strong>)')),
                ('sort_order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Блок методологии',
                'verbose_name_plural': 'Методология',
                'ordering': ['sort_order'],
            },
        ),
    ]
