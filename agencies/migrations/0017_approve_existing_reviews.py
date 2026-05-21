from django.db import migrations


def approve_all(apps, schema_editor):
    """После добавления is_approved все существующие отзывы одобряем."""
    Review = apps.get_model('agencies', 'Review')
    Review.objects.filter(is_approved=False).update(is_approved=True)


def unapprove_all(apps, schema_editor):
    pass  # откат — ничего не делаем


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0016_add_map_coords'),
    ]

    operations = [
        migrations.RunPython(approve_all, unapprove_all),
    ]
