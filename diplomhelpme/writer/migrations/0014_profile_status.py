# Generated by Django 4.2 on 2023-05-12 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writer', '0013_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
