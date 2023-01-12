# Generated by Django 4.1.5 on 2023-01-12 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("likes", "0002_alter_like_object_id"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="like",
            index=models.Index(
                fields=["content_type", "object_id"],
                name="likes_like_content_5c134b_idx",
            ),
        ),
    ]