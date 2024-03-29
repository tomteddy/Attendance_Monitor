# Generated by Django 3.1.1 on 2021-02-02 19:35

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_auto_20210203_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='work_log_id',
            field=models.UUIDField(null=True),
        ),
        migrations.AddField(
            model_name='work_log',
            name='work_log_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='work_log',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.employee'),
        ),
    ]
