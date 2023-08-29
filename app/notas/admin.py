from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.urls import reverse

from notas.models import (
    Servico,
    Trabalho,
    Fechamento,
    Cliente,
    Clinica,
    Clinica_Dentista,
)


# Register your models here.
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['id', 'nome']
    ordering = ['id']


class EntregueListFilter(admin.SimpleListFilter):
    title = 'entregue'

    parameter_name = 'entregue'

    def lookups(self, request, model_admin):
        return (
            ('Sim', 'Sim'),
            ('Não', 'Não'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Não':
            return queryset.filter(entrega=None)
        elif self.value() == 'Sim':
            return queryset.exclude(entrega=None)
        else:
            return queryset.all()


class ClinicaListFilter(admin.SimpleListFilter):
    title = 'clínica'

    parameter_name = 'clinica'

    def lookups(self, request, model_admin):
        return ((c.id, c.nome) for c in Clinica.objects.all())

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(cliente__clinicas__id__contains=self.value())
        else:
            return queryset.all()


@admin.action(description='Fechar nota')
def gera_fechamento(modeladmin, request, queryset):
    clinicas = [t.cliente.clinica for t in queryset]
    if len(set(clinicas)) > 1:
        modeladmin.message_user(
            request=request,
            message='Não é possível gerar um fechamento para várias clinicas.',
            level=messages.ERROR,
        )
        return
    clinica = clinicas[0]
    if sum(t.get_valor_total() for t in queryset) >= clinica.limite_credito - sum(
        t.get_valor_total()
        for t in Trabalho.objects.filter(cliente__clinica=clinica)
        .filter(fechamento__isnull=False)
        .filter(fechamento__data_pagamento__isnull=True)
    ):
        modeladmin.message_user(
            request=request,
            message='Essa clínica tem mais notas em aberto que o seu limite de crédito.',
            level=messages.ERROR,
        )
        return
    fechamento = Fechamento()
    if Fechamento.objects.count() > 0:
        fechamento.nota_de_servico = (
            max(f.nota_de_servico for f in Fechamento.objects.all()) + 1
        )
    else:
        fechamento.nota_de_servico = 1
    fechamento.save()
    queryset.update(fechamento=fechamento)


class TrabalhoAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('fechamento',)
        form = super(TrabalhoAdmin, self).get_form(request, obj, **kwargs)

        return form

    def link_fechamento(self, trabalho):
        if trabalho.fechamento:
            url = reverse(
                "admin:notas_fechamento_change",
                args=[trabalho.fechamento.nota_de_servico],
            )
            link = f'<a href="{url}">{trabalho.fechamento}</a>'
            return mark_safe(link)
        else:
            return '-'

    def link_cliente(self, trabalho):
        url = reverse(
            "admin:notas_clinica_dentista_change",
            args=[trabalho.cliente.id],
        )
        link = f'<a href="{url}">{trabalho.cliente}</a>'
        return mark_safe(link)

    def ultima_atualizacao(self, trabalho):
        if not trabalho.entrega is None:
            return f'Entrega: {trabalho.entrega}'
        elif not trabalho.retorno_3a_prova is None:
            return f'Retorno 3ª Prova: {trabalho.retorno_3a_prova}'
        elif not trabalho.saida_3a_prova is None:
            return f'Saída 3ª Prova: {trabalho.saida_3a_prova}'
        elif not trabalho.retorno_2a_prova is None:
            return f'Retorno 2ª Prova: {trabalho.retorno_2a_prova}'
        elif not trabalho.saida_2a_prova is None:
            return f'Saída 2ª Prova: {trabalho.saida_2a_prova}'
        elif not trabalho.retorno_1a_prova is None:
            return f'Retorno 1ª Prova: {trabalho.retorno_1a_prova}'
        elif not trabalho.saida_1a_prova is None:
            return f'Saída 1ª Prova: {trabalho.saida_1a_prova}'
        else:
            return 'Sem entregas'

    def valor(self, trabalho):
        return trabalho.get_valor_total()

    def trabalho_id(self, trabalho):
        return f'Trabalho {trabalho.id}'

    search_fields = ['servico__nome', 'cliente__nome']
    list_display = [
        'trabalho_id',
        'link_cliente',
        'link_fechamento',
        'paciente',
        'servico',
        'quantidade',
        'elemento',
        'entrada',
        'observacoes',
        'ultima_atualizacao',
        'valor',
    ]
    list_filter = [EntregueListFilter, 'cliente', ClinicaListFilter, 'servico']
    actions = [gera_fechamento]
    date_hierarchy = 'entrada'


class PagoListFilter(admin.SimpleListFilter):
    title = 'pago'

    parameter_name = 'pago'

    def lookups(self, request, model_admin):
        return (
            ('Sim', 'Sim'),
            ('Não', 'Não'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Não':
            return queryset.filter(data_pagamento=None)
        elif self.value() == 'Sim':
            return queryset.exclude(data_pagamento=None)
        else:
            return queryset.all()


class ClienteListFilter(admin.SimpleListFilter):
    title = 'cliente'

    parameter_name = 'cliente'

    def lookups(self, request, model_admin):
        return ((c.nome, c.nome) for c in Cliente.objects.all())

    def queryset(self, request, queryset):
        clientes = [c.nome for c in Cliente.objects.all()]
        if self.value() not in clientes:
            return queryset.all()
        else:
            trabalhos = Trabalho.objects.filter(cliente__nome=self.value())
            notas = [t.fechamento.nota_de_servico for t in trabalhos]
            return queryset.filter(nota_de_servico__in=notas)


class ClinicaListFilter(admin.SimpleListFilter):
    title = 'clínica'

    parameter_name = 'clinica'

    def lookups(self, request, model_admin):
        return ((c.nome, c.nome) for c in Clinica.objects.all())

    def queryset(self, request, queryset):
        clientes = [c.nome for c in Cliente.objects.all()]
        if self.value() not in clientes:
            return queryset.all()
        else:
            trabalhos = Trabalho.objects.filter(cliente__clinica__nome=self.value())
            notas = [t.fechamento.nota_de_servico for t in trabalhos]
            return queryset.filter(nota_de_servico__in=notas)


class FechamentoAdmin(admin.ModelAdmin):
    search_fields = [
        'nota_de_servico',
        'trabalho__cliente__nome',
        'trabalho__cliente__clinicas__nome',
    ]
    list_display = [
        'nota_de_servico',
        'trabalhos',
        'valor_total',
        'vencimento',
        'data_pagamento',
        'gera_nota',
    ]
    list_filter = [PagoListFilter, ClinicaListFilter, ClienteListFilter]
    date_hierarchy = 'vencimento'

    def valor_total(self, fechamento):
        return fechamento.get_soma()

    def trabalhos(self, fechamento):
        trabalhos = Trabalho.objects.filter(fechamento=fechamento)
        links = []
        for trabalho in trabalhos:
            url = reverse(
                "admin:notas_trabalho_change",
                args=[trabalho.id],
            )
            link = f'<a href="{url}">{trabalho}</a>'
            links.append(link)
        return mark_safe(', '.join(links))

    def gera_nota(self, fechamento):
        url = reverse(
            "gera_nota",
            args=[fechamento.nota_de_servico],
        )
        link = f'<a target="_blank" href="{url}">{fechamento}</a>'
        return mark_safe(link)


class ClienteAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'clinicas__nome']
    list_display = ['nome', 'clinica_link', 'clinica_endereco', 'telefones']

    def clinica_link(self, cliente):
        clinicas = Clinica.objects.filter(clientes__nome__contains=cliente.nome)
        links = []
        for clinica in clinicas:
            url = reverse(
                "admin:notas_clinica_change",
                args=[clinica.id],
            )
            link = f'<a href="{url}">{clinica.nome}</a>'
            links.append(link)
        return mark_safe(', '.join(links))

    def clinica_endereco(self, cliente):
        return ', '.join(
            c.endereco
            for c in Clinica.objects.filter(clientes__nome__contains=cliente.nome)
        )


class ClinicaAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'clientes__nome']
    list_display = ['nome', 'dentistas', 'endereco', 'telefones']

    def dentistas(self, clinica):
        clientes = clinica.get_clientes()
        links = []
        for cliente in clientes:
            url = reverse(
                "admin:notas_cliente_change",
                args=[cliente.id],
            )
            link = f'<a href="{url}">{cliente.nome}</a>'
            links.append(link)
        return mark_safe(', '.join(links))


class ClinicaDentistaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Servico, ServicoAdmin)
admin.site.register(Trabalho, TrabalhoAdmin)
admin.site.register(Fechamento, FechamentoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Clinica_Dentista, ClinicaDentistaAdmin)
admin.site.register(Clinica, ClinicaAdmin)

admin.site.site_header = 'Controle do Laboratório'
