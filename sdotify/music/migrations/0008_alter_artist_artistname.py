# Generated by Django 4.2.5 on 2023-11-17 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_alter_album_artist_alter_artist_artistname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='artistName',
            field=models.CharField(max_length=50, verbose_name='Artist Name'),
        ),
    ]
