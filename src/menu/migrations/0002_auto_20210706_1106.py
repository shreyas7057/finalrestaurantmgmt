# Generated by Django 3.2.4 on 2021-07-06 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='num_order',
            new_name='in_stock',
        ),
        migrations.RemoveField(
            model_name='food',
            name='discount',
        ),
    ]