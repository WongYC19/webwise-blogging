# Generated by Django 4.1.5 on 2023-01-10 16:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_alter_comment_options_rename_uuid_post_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
