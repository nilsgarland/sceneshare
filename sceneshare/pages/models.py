from django.db import models
from django.contrib.auth.models import User

class Scene(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    url = models.CharField(max_length=350)
    published = models.DateTimeField('date published')

    def __str__(self):
        return self.url

class Liker(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
