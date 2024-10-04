# Generated by Django 4.2.4 on 2023-10-19 23:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_remove_comment_title_alter_bid_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="timestamp",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
