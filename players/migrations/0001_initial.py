# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-09 22:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid', models.IntegerField()),
                ('status', models.IntegerField(choices=[(0, 'waiting for players'), (1, 'playing'), (2, 'complete')])),
            ],
        ),
        migrations.CreateModel(
            name='GameTurn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='players.Game')),
            ],
            options={
                'ordering': ['-index'],
            },
        ),
        migrations.CreateModel(
            name='GameTurnPlay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('play', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='gameturnplay',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.Player'),
        ),
        migrations.AddField(
            model_name='gameturnplay',
            name='turn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.GameTurn'),
        ),
        migrations.AddField(
            model_name='game',
            name='loser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games_lost', to='players.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(related_name='games', to='players.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games_won', to='players.Player'),
        ),
    ]
