# Generated by Django 5.0.6 on 2024-09-14 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_alter_board_ship_positions'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='in_game',
            field=models.BooleanField(default=False),
        ),
    ]
