# Generated by Django 4.2.3 on 2023-07-31 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notas', '0002_alter_cliente_cpf_alter_cliente_cro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trabalho',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notas.clinica_dentista'),
        ),
    ]
