# Generated by Django 4.1.5 on 2023-01-15 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_alter_post_content_alter_profile_first_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                related_query_name="comment",
                to="blog.post",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(editable=False, max_length=255, unique=True),
        ),
    ]