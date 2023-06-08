from datetime import datetime
from django.shortcuts import render

from .models import Fechamento, Trabalho, Cliente

# Create your views here.
def gera_nota(request, nota_de_servico):
    trabalhos = Trabalho.objects.filter(fechamento__nota_de_servico=nota_de_servico)
    dentistas = sorted(list(set(t.cliente for t in trabalhos)), key=lambda x: x.nome)
    context = {
        'grupos': {
            dentista: {
                'trabalhos': {
                    paciente: [t for t in trabalhos.filter(cliente=dentista).filter(paciente=paciente)]
                    for paciente in (set(t.paciente for t in trabalhos.filter(cliente=dentista)))
                },
                'total': sum(t.get_valor_total() for t in trabalhos.filter(cliente=dentista))
            }
            for dentista in dentistas
        },
        'clinica': dentistas[0].clinica,
        'hoje': datetime.now().date,
        'fechamento': Fechamento.objects.filter(nota_de_servico=nota_de_servico)[0],
    }

    return render(request, 'gera_nota.html', context)
