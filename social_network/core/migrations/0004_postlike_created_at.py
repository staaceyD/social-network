# Generated by Django 5.0.1 on 2024-01-11 20:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_postlike_post_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlike',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
