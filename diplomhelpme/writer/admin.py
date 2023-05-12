from django.contrib import admin
from .models import Content, ContentType, Comment, Like, Profile, PageView
# Register your models here.
admin.site.register(Content)
admin.site.register(ContentType)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Profile)
admin.site.register(PageView)

