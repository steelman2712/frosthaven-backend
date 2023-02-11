# Generated by Django 4.1.6 on 2023-02-10 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_abilitycard_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='characterperk',
            name='active',
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(null=True, upload_to='items/'),
        ),
        migrations.AddField(
            model_name='perk',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='perk',
            name='image',
            field=models.ImageField(null=True, upload_to='perks/'),
        ),
        migrations.AddField(
            model_name='perk',
            name='max_uses',
            field=models.IntegerField(default=1),
        ),
    ]