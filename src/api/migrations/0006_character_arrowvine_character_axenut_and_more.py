# Generated by Django 4.1.6 on 2023-02-09 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_perk_characterperk'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='arrowvine',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='axenut',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='corpsecap',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='flamefruit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='rockroot',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='snowthistle',
            field=models.IntegerField(default=0),
        ),
    ]
