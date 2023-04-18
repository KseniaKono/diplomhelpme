from django.contrib import admin
from .models import Content, ContentType, Comment
# Register your models here.
admin.site.register(Content)
admin.site.register(ContentType)
admin.site.register(Comment)