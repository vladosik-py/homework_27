from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Ad(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=200)
    is_published = models.BooleanField(default=False)
