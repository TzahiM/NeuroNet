# Generated by Django 2.2.7 on 2020-05-07 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memecache', '0002_auto_20200421_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='picture',
            field=models.ImageField(blank=True, default=None, max_length=500000, null=True, upload_to='uploads/%Y/%m/%d/', verbose_name='A picture that describe the product'),
        ),
    ]