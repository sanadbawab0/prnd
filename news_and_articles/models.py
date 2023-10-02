from django.db import models
from user.models import Profile
import uuid
from django.utils import timezone


# Create your models here.
class NewsAndArticles(models.Model):
    title = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE, related_name='author')
    image = models.ImageField(
        upload_to='NewsAndArticles', blank=True, null=True)
    content = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    post_time = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        ordering = ['-post_time']

    def __str__(self):
        return f"{self.title}"

    @property
    def get_reviews(self):
        return NewsAndArticlesReview.objects.filter(news_article=self)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f'{self.id}'
        super().save(*args, **kwargs)


class NewsAndArticlesReview(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='reviewd_by')
    news_article = models.ForeignKey(
        NewsAndArticles, null=True, on_delete=models.CASCADE, related_name='article_reviews')
    content = models.TextField(blank=True, null=True)
    # like = models.BooleanField(default=False)
    review_date = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        ordering = ['-review_date']

    def __str__(self):
        return f"{self.user} reviewed {self.news_article.author}"
