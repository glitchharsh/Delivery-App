# Generated by Django 4.1.5 on 2023-01-13 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_delete_matchedassets'),
    ]

    operations = [
        migrations.AddField(
            model_name='ridertravelinfo',
            name='status',
            field=models.CharField(choices=[('APPLIED', 'APPLIED'), ('NOT_APPLIED', 'NOT_APPLIED')], default='PENDING', max_length=20),
        ),
        migrations.CreateModel(
            name='MatchedAssets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applied', models.BooleanField(default=True)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.transportrequest')),
                ('rider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='delivery.ridertravelinfo')),
            ],
        ),
    ]
