import json
from django.shortcuts import render
from core import models
from .models import Ecopontos


import json
from django.shortcuts import render
from core import models
from .models import Ecopontos


def dashboard(request):
    # Trata cada busca independentemente para evitar Erro 500 em produção
    try:
        metricas = models.VwDashboardMetricas.objects.first()
    except Exception:
        metricas = None

    try:
        ecopontos = models.Ecopontos.objects.filter(ativo=True)
    except Exception:
        ecopontos = []

    try:
        materiais = models.Materiais.objects.all()
    except Exception:
        materiais = []

    context = {
        "metricas": metricas,
        "ecopontos": ecopontos,
        "materiais": materiais,
    }

    return render(request, "core/dashboard.html", context)


def login_view(request):
    """
    Renderiza a tela de login.
    """
    return render(request, "core/login.html")


def mapa_ecopontos(request):
    """
    Renderiza o mapa serializando as coordenadas dos Ecopontos ativos para JSON.
    """
    ecopontos = Ecopontos.objects.filter(ativo=True)

    ecopontos_data = [
        {
            "nome": e.nome,
            "bairro": e.bairro,
            "cidade": e.cidade,
            "endereco": e.endereco,
            "lat": float(e.latitude) if e.latitude else None,
            "lng": float(e.longitude) if e.longitude else None,
        }
        for e in ecopontos
    ]

    context = {"ecopontos_json": json.dumps(ecopontos_data)}
    return render(request, "core/mapa.html", context)
