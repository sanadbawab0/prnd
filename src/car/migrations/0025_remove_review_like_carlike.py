# Generated by Django 4.2.4 on 2023-08-30 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('car', '0024_exteriorimage_interiorimage_delete_imagemodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='like',
        ),
        migrations.CreateModel(
            name='CarLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='car.car')),
                ('liked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
            ],
        ),
    ]
