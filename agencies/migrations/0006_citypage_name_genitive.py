from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0005_citypage'),
    ]

    operations = [
        migrations.AddField(
            model_name='citypage',
            name='name_genitive',
            field=models.CharField(
                default='',
                help_text='Например: Санкт-Петербурга — используется в заголовке «Агентства …»',
                max_length=100,
                verbose_name='Город (родительный падеж)',
            ),
        ),
    ]
