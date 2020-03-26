# Generated by Django 2.2.7 on 2019-11-26 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_name', models.CharField(default='', max_length=200)),
                ('family_name', models.CharField(default='', max_length=200)),
                ('email', models.EmailField(blank=True, max_length=70)),
                ('phone_number', models.CharField(default='', max_length=17)),
                ('url', models.URLField(blank=True, default='http://kuterless.org.il', max_length=2000)),
                ('score', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Acquaintance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('message', models.CharField(default='', max_length=2000)),
                ('is_played', models.BooleanField(default=False)),
                ('business_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nice_to_meet_you.BusinessCard')),
            ],
        ),
    ]
