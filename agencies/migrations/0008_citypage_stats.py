from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0007_sitesettings_stats'),
    ]

    operations = [
        migrations.AddField(model_name='citypage', name='stat1_value',
            field=models.CharField(default='100+', max_length=20, verbose_name='Стат 1 — число')),
        migrations.AddField(model_name='citypage', name='stat1_label',
            field=models.CharField(default='проверенных\nагентств', max_length=60, verbose_name='Стат 1 — подпись')),
        migrations.AddField(model_name='citypage', name='stat2_value',
            field=models.CharField(default='4', max_length=20, verbose_name='Стат 2 — число')),
        migrations.AddField(model_name='citypage', name='stat2_label',
            field=models.CharField(default='критерия\nоценки', max_length=60, verbose_name='Стат 2 — подпись')),
        migrations.AddField(model_name='citypage', name='stat3_value',
            field=models.CharField(default='12', max_length=20, verbose_name='Стат 3 — число')),
        migrations.AddField(model_name='citypage', name='stat3_label',
            field=models.CharField(default='месяцев\nисследования', max_length=60, verbose_name='Стат 3 — подпись')),
        migrations.AddField(model_name='citypage', name='stat4_value',
            field=models.CharField(default='0₽', max_length=20, verbose_name='Стат 4 — число')),
        migrations.AddField(model_name='citypage', name='stat4_label',
            field=models.CharField(default='платных\nразмещений', max_length=60, verbose_name='Стат 4 — подпись')),
    ]
