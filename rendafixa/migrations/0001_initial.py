# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-15 13:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('crawler_name', models.CharField(default='', max_length=200)),
                ('identifier', models.CharField(max_length=100, unique=True)),
                ('expiration_date', models.DateTimeField(verbose_name='Expiration date')),
                ('term_days', models.BigIntegerField(default=0)),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Last update')),
            ],
        ),
        migrations.CreateModel(
            name='BoundData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('buy_tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sell_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sell_tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('bound', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rendafixa.Bound')),
            ],
        ),
        migrations.CreateModel(
            name='BoundType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('identifier', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Issuer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('identifier', models.CharField(max_length=100, unique=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='bound',
            name='bound_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rendafixa.BoundType'),
        ),
        migrations.AddField(
            model_name='bound',
            name='issuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rendafixa.Issuer'),
        ),
    ]