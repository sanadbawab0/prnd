# Generated by Django 4.2.4 on 2023-09-02 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_favorite_cars_profile_favorite_posts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='favorite_posts',
            new_name='favorite_cars',
        ),
    ]
