# Generated by Django 5.1.3 on 2025-03-18 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_usernew'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernew',
            name='profile_pic',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
