# Generated by Django 4.0.3 on 2022-06-18 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FamilyCreate', '0004_remove_my_users_room_alter_my_room_name_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='id_room',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='FamilyCreate.users_room'),
        ),
    ]