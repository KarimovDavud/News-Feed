from django.contrib.auth.models import User
from django.db import models

class Feed(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    youtube_video_url = models.URLField(blank=True, null=True)
    view_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='feed_images/', null=True, blank=True)  # Resim alanı

    def __str__(self):
        return self.title

class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    like = models.BooleanField()  # True for like, False for dislike
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'feed')
