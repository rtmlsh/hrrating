from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0019_resumeconstructorpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumeconstructorfaq',
            name='page',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='faq_items',
                to='agencies.resumeconstructorpage',
                verbose_name='Страница',
            ),
        ),
    ]
