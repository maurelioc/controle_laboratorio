# Generated by Django 4.2.3 on 2023-08-09 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notas', '0005_trabalho_cor_alter_trabalho_elemento'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='clinica_dentista',
            unique_together={('cliente', 'clinica')},
        ),
    ]
