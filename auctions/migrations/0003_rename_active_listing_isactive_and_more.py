# Generated by Django 4.2.13 on 2024-06-25 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_rename_time_bid_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='active',
            new_name='isActive',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='highest_bid',
        ),
        migrations.AddField(
            model_name='listing',
            name='highestBid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='listing',
            name='startingBid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
