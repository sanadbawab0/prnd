# Generated by Django 4.2.4 on 2023-08-26 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0006_alter_pricehistory_car'),
    ]

    operations = [
        migrations.RenameField(
            model_name='techandsafetyfeatures',
            old_name='feature',
            new_name='features',
        ),
    ]