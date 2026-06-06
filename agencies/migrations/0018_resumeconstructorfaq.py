from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0017_approve_existing_reviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResumeConstructorFaq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300, verbose_name='Вопрос')),
                ('answer', models.TextField(verbose_name='Ответ')),
                ('sort_order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'FAQ конструктора резюме',
                'verbose_name_plural': 'FAQ конструктора резюме',
                'ordering': ['sort_order'],
            },
        ),
    ]
