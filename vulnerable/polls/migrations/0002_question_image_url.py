# Generated by Django 4.1.7 on 2023-04-17 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='image_url',
            field=models.CharField(default='', max_length=200),
        ),
    ]
