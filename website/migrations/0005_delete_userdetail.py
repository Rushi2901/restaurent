# Generated by Django 5.1.2 on 2024-10-27 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_footer_userdetail'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserDetail',
        ),
    ]