# Generated by Django 3.2.12 on 2022-06-19 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_ad_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='images',
        ),
    ]
