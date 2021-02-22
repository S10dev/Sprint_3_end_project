from django.db import models

# Create your models here.
class Disk(models.Model):
    artist = models.CharField(max_length=100)

    def __str__(self):
        return self.artist