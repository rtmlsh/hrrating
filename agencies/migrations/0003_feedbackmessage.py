from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0002_add_sitesettings_citylink'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('subject', models.CharField(blank=True, max_length=200, verbose_name='Тема')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('is_read', models.BooleanField(default=False, verbose_name='Прочитано')),
            ],
            options={
                'verbose_name': 'Обращение',
                'verbose_name_plural': 'Обращения',
                'ordering': ['-created_at'],
            },
        ),
    ]
