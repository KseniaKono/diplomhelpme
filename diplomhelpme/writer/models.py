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
    similar_content = models.ManyToManyField('self', blank=True, verbose_name='Похожие произведения')

    def __str__(self):
        return '%s (%s)' % (self.name, str(self.id))

    def get_absolute_url(self):
        return reverse('contentdetail', args=[str(self.id)])


class SimilarityVote(models.Model):
    VOTE_CHOICES = (
        ('+', 'Похоже'),
        ('-', 'Не похоже'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='source_votes', null=True)
    target_content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='target_votes', null=True)
    vote = models.CharField(max_length=1, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'source_content', 'target_content')

    def __str__(self):
        return f"{self.user.username} - {self.vote} - {self.source_content.name} - {self.target_content.name}"


class ContentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный id для каждого жанра')
    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание', max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный id для каждого комментария')
    commentator = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name='Произведение')
    text = models.TextField('Текст', max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('comment-detail')


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный id для каждой оценки')
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name='Произведение')
    def __str__(self):
        return str(self.id)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    location = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=200, null=True, blank=True)
    interests = models.CharField(max_length=200, null=True, blank=True)
    skills = models.CharField(max_length=200, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class PageView(models.Model):
    page_url = models.CharField(max_length=255)
    views_count = models.IntegerField(default=0)
