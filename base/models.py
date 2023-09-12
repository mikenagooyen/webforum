from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.name)


class Thread(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    post = models.TextField()
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return str(self.name)
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    post = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.post[0:50]