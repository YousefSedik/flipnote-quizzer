# Generated by Django 5.1.6 on 2025-04-13 09:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_alter_quiz_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="views_count",
            field=models.SmallIntegerField(db_index=True, default=0),
        ),
    ]
