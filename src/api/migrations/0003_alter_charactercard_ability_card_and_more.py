# Generated by Django 4.1.6 on 2023-02-18 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_flip_description_item_flipdescription_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charactercard',
            name='ability_card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character', to='api.abilitycard'),
        ),
        migrations.AlterField(
            model_name='charactercard',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='api.character'),
        ),
        migrations.AlterField(
            model_name='characteritem',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.character'),
        ),
        migrations.AlterField(
            model_name='characterperk',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perks', to='api.character'),
        ),
    ]
