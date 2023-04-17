# Generated by Django 4.2 on 2023-04-17 16:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('writer', '0002_alter_contenttype_id_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenttype',
            name='id',
            field=models.UUIDField(default=uuid.UUID('ee235d3d-74c1-434e-b80f-4755154f0b97'), help_text='Уникальный id для каждого жанра', primary_key=True, serialize=False),
        ),
    ]