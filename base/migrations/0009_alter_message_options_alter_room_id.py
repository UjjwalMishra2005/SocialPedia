# Generated by Django 5.1.3 on 2025-01-23 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_room_participants'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-created', '-updated']},
        ),
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
