# Generated by Django 4.1.9 on 2023-07-30 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userhistory',
            name='bid',
        ),
        migrations.RemoveField(
            model_name='userhistory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='userhistory',
            name='listing_image',
        ),
        migrations.RemoveField(
            model_name='userhistory',
            name='listing_name',
        ),
        migrations.RemoveField(
            model_name='userhistory',
            name='price',
        ),
    ]
