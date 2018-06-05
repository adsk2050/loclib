# Generated by Django 2.0.5 on 2018-06-04 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20180604_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='borrower',
            field=models.ForeignKey(default='lib', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
