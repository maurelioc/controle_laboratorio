# Generated by Django 4.2.3 on 2023-08-16 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notas', '0006_alter_clinica_dentista_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabalho',
            name='desconto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='trabalho',
            name='taxa_urgencia',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]