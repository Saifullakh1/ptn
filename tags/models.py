from django.db import models
from posts.models import Post


class Tag(models.Model):
    title = models.CharField(max_length=255)
    posts = models.ManyToManyField(Post, verbose_name='tags')

    def __str__(self):
        return f"{self.title} -- Post's title == {self.posts}"



