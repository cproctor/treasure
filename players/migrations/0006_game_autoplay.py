# Generated by Django 2.0.2 on 2018-02-20 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0005_auto_20180216_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='autoplay',
            field=models.BooleanField(default=False),
        ),
    ]
