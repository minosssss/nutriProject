# Generated by Django 3.2.9 on 2021-11-12 14:16

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_code', models.CharField(max_length=50, unique=True)),
                ('age_category', models.IntegerField(choices=[(1929, '19~29'), (3049, '30~49'), (5064, '50~64')])),
                ('carb', models.FloatField(blank=True)),
                ('prot', models.FloatField(blank=True)),
                ('fat', models.FloatField(blank=True)),
                ('sodium', models.FloatField(blank=True)),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (2, 'Female')])),
            ],
            options={
                'db_table': 'nutri_standard',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
                ('age_category', models.IntegerField(choices=[(1929, '19~29'), (3049, '30~49'), (5064, '50~64')])),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (2, 'Femail')])),
                ('activity', models.FloatField(choices=[(1.2, '거의 없음'), (1.375, '활동량 조금있다.(주1~2회 운동)'), (1.55, '활동량 많다.(주3~5회 운동)'), (1.725, '활동량 꽤 많다.(주6~7회 운동)'), (1.9, '활동량 아주 많다.(매일 2번 운동)')])),
                ('proper_cal', models.FloatField(blank=True)),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('update_dt', models.DateTimeField(auto_now=True)),
                ('n_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.standard')),
            ],
            options={
                'db_table': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
