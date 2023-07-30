# Generated by Django 4.1.9 on 2023-07-29 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardholder_name', models.CharField(max_length=100)),
                ('card_number', models.CharField(max_length=16)),
                ('expiry_month', models.IntegerField()),
                ('expiry_year', models.IntegerField()),
                ('cvc', models.CharField(max_length=4)),
                ('iban_number', models.CharField(max_length=34)),
            ],
        ),
    ]
