# Generated by Django 4.2.6 on 2023-11-06 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medprob', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bp',
            options={'ordering': ['-date_num', 'time_num']},
        ),
    ]
