# Generated by Django 4.2.3 on 2023-07-29 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cpf',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cro',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
