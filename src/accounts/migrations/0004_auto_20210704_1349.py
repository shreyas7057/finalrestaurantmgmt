# Generated by Django 3.2.4 on 2021-07-04 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_auto_20210704_0637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='id',
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
