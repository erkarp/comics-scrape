# Generated by Django 2.1.5 on 2020-06-08 00:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plant',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='species',
            options={'ordering': ['name'], 'verbose_name_plural': 'species'},
        ),
        migrations.AlterModelOptions(
            name='watering',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='shop',
            name='closed_down',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='watering',
            name='fertilized',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='plant',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='plants.Shop'),
        ),
        migrations.AlterField(
            model_name='species',
            name='fertilize_frequency',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='species',
            name='fertilizer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='plants.Fertilizer'),
        ),
        migrations.AlterField(
            model_name='watering',
            name='date',
            field=models.DateField(default=datetime.date.today, unique=True),
        ),
    ]
