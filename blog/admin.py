from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Post, Comment, Member

# Register your models here.

admin.site.register(MyUser, UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Member)