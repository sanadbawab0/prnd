# Generated by Django 4.2.4 on 2023-08-26 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0007_rename_feature_techandsafetyfeatures_features'),
    ]

    operations = [
        migrations.RenameField(
            model_name='techandsafetyfeatures',
            old_name='features',
            new_name='feature',
        ),
    ]