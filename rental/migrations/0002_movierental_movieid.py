# Generated by Django 2.0.2 on 2018-03-05 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movierental',
            name='movieId',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
