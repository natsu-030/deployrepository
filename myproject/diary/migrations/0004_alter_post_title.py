# Generated by Django 5.0.3 on 2024-04-11 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0003_remove_post_content_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]
