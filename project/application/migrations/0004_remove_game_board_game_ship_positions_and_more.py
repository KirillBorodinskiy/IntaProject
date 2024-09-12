# Generated by Django 5.0.6 on 2024-09-12 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_shipposition_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='board',
        ),
        migrations.AddField(
            model_name='game',
            name='ship_positions',
            field=models.JSONField(default=list),
        ),
        migrations.DeleteModel(
            name='ShipPosition',
        ),
    ]