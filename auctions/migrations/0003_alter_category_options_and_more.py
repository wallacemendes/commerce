# Generated by Django 4.2.4 on 2023-10-04 01:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0002_category_listing_comment_bid"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "categories"},
        ),
        migrations.RenameField(
            model_name="listing",
            old_name="status",
            new_name="is_active",
        ),
    ]
