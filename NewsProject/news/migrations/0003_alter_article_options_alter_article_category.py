# Generated by Django 4.2.8 on 2023-12-21 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0002_article_category"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={
                "ordering": ["date", "title"],
                "verbose_name": "Новость",
                "verbose_name_plural": "Новости",
            },
        ),
        migrations.AlterField(
            model_name="article",
            name="category",
            field=models.CharField(
                choices=[("E", "Economic"), ("S", "Science"), ("I", "IT")],
                max_length=20,
                verbose_name="Категории",
            ),
        ),
    ]
