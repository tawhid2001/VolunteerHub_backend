# Generated by Django 4.2 on 2024-09-02 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='./core/image/default_profile.jpg', upload_to='profile_pics/'),
        ),
    ]
