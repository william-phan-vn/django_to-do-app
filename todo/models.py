from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    is_important = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    completed_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
