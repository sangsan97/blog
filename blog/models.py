from django.db import models
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    StudentID = models.CharField(max_length=10)

class Member(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    where_to = [
        ('postdoc', 'Post Doctorate'),
        ('phd', 'PhD.'),
        ('master', 'Master Degree'),
        ('visiting', 'Visiting Student'),
    ]
    where_to_status = models.CharField(max_length=20, choices=where_to, default='master')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('members')

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey('MyUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    document = models.FileField(blank=True, null=True, upload_to='documents/')
    where_to = [
        ('post_list', 'Post List'),
        ('post_list2', 'Post List2'),
        ('draft', 'Draft')
    ]
    where_to_status = models.CharField(max_length=15, choices=where_to, default='draft')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comment(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text

class Publication(models.Model):
    title = models.CharField(max_length=500)
    explanation_for_the_publication = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    year_of_publication = models.DateTimeField(blank=False)
    link_url = models.URLField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return str(self.title)