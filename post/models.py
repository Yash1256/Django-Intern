from django.db import models
from registration.models import Author


# Create your models here.
class Post(models.Model):
    author_id = models.IntegerField(null=False)
    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=500, null=False)
    content = models.TextField(null=False)
    date = models.DateField(null=False)

    class Meta:
        db_table = "posts"
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    @property
    def author(self):
        return Author.objects.get(pk=self.author_id)

    def __str__(self):
        return f"{self.title}({self.author.name})"
