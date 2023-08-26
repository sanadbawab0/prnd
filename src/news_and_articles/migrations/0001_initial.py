# Generated by Django 4.2.4 on 2023-08-23 12:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsAndArticles',
            fields=[
                ('title', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='NewsAndArticles')),
                ('content', models.TextField(blank=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('post_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author', to='user.profile')),
                ('liked_by', models.ManyToManyField(blank=True, default=None, to='user.profile')),
            ],
            options={
                'ordering': ['-post_time'],
            },
        ),
        migrations.CreateModel(
            name='NewsAndArticlesReview',
            fields=[
                ('content', models.TextField(blank=True, null=True)),
                ('like', models.BooleanField(default=False)),
                ('review_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('news_article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_reviews', to='news_and_articles.newsandarticles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewd_by', to='user.profile')),
            ],
            options={
                'ordering': ['-review_date'],
            },
        ),
    ]