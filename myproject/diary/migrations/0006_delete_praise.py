# Generated by Django 5.0.3 on 2024-04-13 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0005_remove_post_likes_post_likes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Praise',
        ),
    ]
