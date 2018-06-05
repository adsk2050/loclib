# Generated by Django 2.0.5 on 2018-06-02 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20180602_1811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='genres',
        ),
        migrations.RemoveField(
            model_name='author',
            name='languages',
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Born'),
        ),
    ]
