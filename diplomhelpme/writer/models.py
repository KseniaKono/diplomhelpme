from django.db import models
import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный id для каждого произведения')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    ganre = models.ForeignKey('ContentType', on_delete=models.SET_NULL, null=True, verbose_name='Жанр')
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Аннотация', max_length=500, null=True)
    data = models.TextField('Текст')

    def __str__(self):
        return '%s (%s)' % (self.name, str(self.id))

    def get_absolute_url(self):
        return reverse('contentdetail', args=[str(self.id)])



class ContentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный id для каждого жанра')
    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание', max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный id для каждой оценки')
    commentator = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name='Произведение')
    text = models.TextField('Текст', max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('comment-detail')
