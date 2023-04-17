# Generated by Django 4.2 on 2023-04-17 16:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('writer', '0003_alter_contenttype_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='ganre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='writer.contenttype', verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='id',
            field=models.UUIDField(default=uuid.UUID('9d4fc544-f12f-4bd6-82a3-35c8e55c2215'), help_text='Уникальный id для каждого жанра', primary_key=True, serialize=False),
        ),
    ]
