from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date


class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    video_image = models.ImageField(
        upload_to='video_images', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'netflixapp_video'
