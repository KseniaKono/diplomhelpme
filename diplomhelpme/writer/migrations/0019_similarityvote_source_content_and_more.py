# Generated by Django 4.2 on 2023-05-15 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('writer', '0018_content_similar_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='similarityvote',
            name='source_content',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_votes', to='writer.content'),
        ),
        migrations.AddField(
            model_name='similarityvote',
            name='target_content',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_votes', to='writer.content'),
        ),
        migrations.AlterUniqueTogether(
            name='similarityvote',
            unique_together={('user', 'source_content', 'target_content')},
        ),
        migrations.RemoveField(
            model_name='similarityvote',
            name='content',
        ),
    ]
