# Generated by Django 2.0.5 on 2018-06-05 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_auto_20180605_1335'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_list_all_borrowed', 'List all borrowed books'), ('can_return', 'Return issued books'), ('can_renew', 'Renew issued books'), ('can_issue', 'Issue Books'))},
        ),
    ]
