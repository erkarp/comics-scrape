# Generated by Django 2.1.5 on 2020-08-30 16:31

from django.db import migrations


def create_rooms(apps, schema_editor):
    Room = apps.get_model('plants', 'Room')

    [Room.objects.create(name=room) for room in [
        'Bedroom',
        'Kitchen',
        'Living room',
        'Office',
    ]]


def delete_rooms(apps, schema_editor):
    Room = apps.get_model('plants', 'Room')
    Room.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0008_auto_20200830_1230'),
    ]

    operations = [
        migrations.RunPython(create_rooms, delete_rooms)
    ]
