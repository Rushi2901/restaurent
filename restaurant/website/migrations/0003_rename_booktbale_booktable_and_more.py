# Generated by Django 5.1.2 on 2024-10-11 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_offersection'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BookTbale',
            new_name='BookTable',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='description',
            new_name='review',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='user_name',
        ),
        migrations.AddField(
            model_name='feedback',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='feedback',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]