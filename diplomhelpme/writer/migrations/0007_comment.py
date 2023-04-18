# Generated by Django 4.2 on 2023-04-18 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('writer', '0006_alter_contenttype_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный id для каждой оценки', primary_key=True, serialize=False)),
                ('text', models.TextField(max_length=500, verbose_name='Текст')),
                ('commentator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('content_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='writer.content', verbose_name='Произведение')),
            ],
        ),
    ]