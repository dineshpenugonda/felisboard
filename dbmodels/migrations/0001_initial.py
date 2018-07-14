# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-12 07:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_name', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('building_number', models.CharField(max_length=10)),
                ('postal_code', models.CharField(max_length=10)),
                ('locality', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'post',
            },
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('reaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('reaction_type', models.CharField(choices=[(b'L', b'Like'), (b'D', b'Dislike')], max_length=1)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbmodels.Post')),
            ],
            options={
                'db_table': 'reaction',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=150)),
                ('user_id', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AddField(
            model_name='reaction',
            name='reacted_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbmodels.User'),
        ),
        migrations.AddField(
            model_name='post',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbmodels.User'),
        ),
    ]
