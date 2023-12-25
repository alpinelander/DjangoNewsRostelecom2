# Generated by Django 4.2.8 on 2023-12-21 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0003_alter_article_options_alter_article_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=80)),
                ("status", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
                "ordering": ["title", "status"],
            },
        ),
        migrations.AddField(
            model_name="article",
            name="tags",
            field=models.ManyToManyField(blank=True, to="news.tag"),
        ),
    ]
