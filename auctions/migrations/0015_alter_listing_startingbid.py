# Generated by Django 4.2.13 on 2024-06-29 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_listing_highestbid_alter_listing_startingbid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='startingBid',
            field=models.FloatField(default=0),
        ),
    ]
