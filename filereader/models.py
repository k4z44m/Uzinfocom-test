from django.db import models


class Repository(models.Model):
    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    stars = models.IntegerField()
    forks = models.IntegerField()
    created_at = models.DateTimeField()
    
class RepositoryLanguage(models.Model):
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="languages"
    )
    name = models.CharField(max_length=100)
    size = models.IntegerField()

