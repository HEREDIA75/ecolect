import json
from django.shortcuts import render
from core import models
from .models import Ecopontos  # Import correto no plural


def dashboard(request):
    # Tenta buscar das views se existirem, caso contrário busca das models principais
    try:
        metricas = models.VwDashboardMetricas.objects.first()
    except AttributeError:
        metricas = None

    ecopontos = models.Ecopontos.objects.filter(ativo=True)
    materiais = models.Materiais.objects.all()

    context = {
        "metricas": metricas,
        "ecopontos": ecopontos,
        "materiais": materiais,
    }

    if request.htmx:
        return render(request, "core/partials/metricas_cards.html", context)

    return render(request, "core/dashboard.html", context)


def login_view(request):
    return render(request, "core/login.html")


def mapa_ecopontos(request):
    # Buscar os ecopontos ativos
    ecopontos = Ecopontos.objects.filter(ativo=1)

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
