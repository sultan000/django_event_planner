# Generated by Django 2.1.7 on 2019-02-27 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20190226_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='capacity',
            field=models.IntegerField(),
        ),
    ]
