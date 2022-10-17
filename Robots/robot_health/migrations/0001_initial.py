# Generated by Django 4.1 on 2022-10-17 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RobotNun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('state', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'robot_num',
            },
        ),
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=32)),
                ('time_set', models.DateTimeField()),
                ('r_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='robot_health.robotnun')),
            ],
        ),
    ]
