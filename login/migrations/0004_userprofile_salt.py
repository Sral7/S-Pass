# Generated by Django 4.2.5 on 2023-09-17 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_userprofile_hashed_pin'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='salt',
            field=models.BinaryField(default=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', max_length=16),
        ),
    ]
