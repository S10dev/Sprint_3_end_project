# Generated by Django 2.2.9 on 2021-03-07 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_auto_20210307_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(help_text='Текст комменатрия', max_length=100),
        ),
    ]