from django.db import models


class Category(models.Model):
    name       = models.CharField(max_length=100)
    slug       = models.SlugField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    bio        = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title      = models.CharField(max_length=300)
    slug       = models.SlugField(max_length=300,unique=True)
    content    = models.TextField()
    author     = models.ForeignKey(
                     Author,
                     on_delete=models.SET_NULL,
                     null=True,
                     blank=True,
                 )
    category   = models.ForeignKey(
                     Category,
                     on_delete=models.SET_NULL,
                     null=True,
                     blank=True,
                 )
    is_published = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title