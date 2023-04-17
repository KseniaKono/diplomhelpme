# Generated by Django 4.2 on 2023-04-17 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('writer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenttype',
            name='id',
            field=models.UUIDField(default=uuid.UUID('49fedd5d-67aa-4da9-b5ec-a0a20fd95414'), help_text='Уникальный id для каждого жанра', primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный id для каждого произведения', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(max_length=500, null=True, verbose_name='Аннотация')),
                ('data', models.TextField(verbose_name='Текст')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
    ]
