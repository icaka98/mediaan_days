# Generated by Django 2.1.3 on 2018-11-03 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_days', '0003_auto_20181103_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(verbose_name='work day')),
                ('hours', models.IntegerField(default=8)),
            ],
        ),
    ]
