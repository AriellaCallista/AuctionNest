# Generated by Django 4.2.13 on 2024-06-26 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='highestBid',
            field=models.DecimalField(decimal_places=2, default=models.DecimalField(decimal_places=2, default=0, max_digits=20), max_digits=20),
        ),
    ]
