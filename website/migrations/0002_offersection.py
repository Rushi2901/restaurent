# Generated by Django 5.1.2 on 2024-10-11 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offersection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('percent_off', models.IntegerField()),
                ('image', models.ImageField(upload_to='items/')),
            ],
        ),
    ]
