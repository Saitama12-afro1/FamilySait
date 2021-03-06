# Generated by Django 4.0.3 on 2022-06-22 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FamilyCreate', '0006_alter_task_id_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='Taken_User_Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FamilyCreate.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'taken_user_task_',
            },
        ),
    ]
