# Generated by Django 2.2.9 on 2021-03-07 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0021_auto_20210307_0749'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set(),
        ),
    ]
