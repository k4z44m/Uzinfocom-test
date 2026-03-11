from django.db import models


class Repository(models.Model):
    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    stars = models.IntegerField()
    forks = models.IntegerField()
    primary_language = models.CharField(max_length=100, null=True, blank=True,db_index=True) # индекс добавил для ускорения
    created_at = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"{self.owner}/{self.name}"