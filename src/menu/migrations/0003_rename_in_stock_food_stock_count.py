# Generated by Django 3.2.4 on 2021-07-06 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20210706_1106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='in_stock',
            new_name='stock_count',
        ),
    ]
