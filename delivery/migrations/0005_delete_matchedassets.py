# Generated by Django 4.1.5 on 2023-01-13 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_remove_ridertravelinfo_status_matchedassets'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MatchedAssets',
        ),
    ]
