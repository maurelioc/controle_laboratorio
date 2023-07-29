# Generated by Django 4.2.3 on 2023-07-29 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('cro', models.CharField(max_length=50)),
                ('cpf', models.CharField(max_length=20)),
                ('telefones', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Clinica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('cnpj', models.CharField(max_length=50)),
                ('insc_estadual', models.CharField(blank=True, max_length=50, null=True)),
                ('insc_municipal', models.CharField(blank=True, max_length=50, null=True)),
                ('endereco', models.CharField(max_length=200)),
                ('telefones', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fechamento',
            fields=[
                ('nota_de_servico', models.IntegerField(primary_key=True, serialize=False)),
                ('vencimento', models.DateField(blank=True, null=True)),
                ('data_pagamento', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Serviço',
                'verbose_name_plural': 'Serviços',
            },
        ),
        migrations.CreateModel(
            name='Trabalho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paciente', models.CharField(max_length=200)),
                ('quantidade', models.IntegerField()),
                ('elemento', models.CharField(blank=True, max_length=50, null=True)),
                ('entrada', models.DateField()),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('saida_1a_prova', models.DateField(blank=True, null=True)),
                ('retorno_1a_prova', models.DateField(blank=True, null=True)),
                ('saida_2a_prova', models.DateField(blank=True, null=True)),
                ('retorno_2a_prova', models.DateField(blank=True, null=True)),
                ('saida_3a_prova', models.DateField(blank=True, null=True)),
                ('retorno_3a_prova', models.DateField(blank=True, null=True)),
                ('entrega', models.DateField(blank=True, null=True)),
                ('valor_unitario', models.DecimalField(decimal_places=2, max_digits=20)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notas.cliente')),
                ('fechamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='notas.fechamento')),
                ('servico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notas.servico')),
            ],
        ),
        migrations.CreateModel(
            name='Clinica_Dentista',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notas.cliente')),
                ('clinica', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notas.clinica')),
            ],
            options={
                'verbose_name': 'Relação Dentista-Clínica',
                'verbose_name_plural': 'Relações Dentista-Clínica',
            },
        ),
        migrations.AddField(
            model_name='clinica',
            name='clientes',
            field=models.ManyToManyField(through='notas.Clinica_Dentista', to='notas.cliente'),
        ),
        migrations.AddField(
            model_name='clinica',
            name='contato',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contato_da_clinica', to='notas.cliente'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='clinicas',
            field=models.ManyToManyField(through='notas.Clinica_Dentista', to='notas.clinica'),
        ),
    ]
