from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Usuarios,
    Perfis,
    Ecopontos,
    Materiais,
    Coletas,
    ItensColeta,
    Recompensas,
    Resgates,
    VwDashboardMetricas,
)


@admin.register(Perfis)
class PerfisAdmin(admin.ModelAdmin):
    list_display = ("id_perfil", "nome")
    search_fields = ("nome",)


@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = (
        "id_usuario",
        "nome",
        "email",
        "cpf",
        "saldo_pontos",
        "id_perfil",
        "criado_em",
    )
    search_fields = ("nome", "email", "cpf")
    list_filter = ("id_perfil", "criado_em")
    readonly_fields = ("id_usuario", "criado_em")
    autocomplete_fields = ("id_perfil",)


@admin.register(Ecopontos)
class EcopontosAdmin(admin.ModelAdmin):
    list_display = ("id_ecoponto", "nome", "bairro", "cidade", "exibir_status")
    list_filter = ("ativo", "cidade")
    search_fields = ("nome", "cidade", "bairro", "endereco")

    @admin.display(description="Status")
    def exibir_status(self, obj):
        if obj.ativo == 1:
            return format_html(
                '<span style="color: green; font-weight: bold;">Ativo</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">Inativo</span>'
        )


@admin.register(Materiais)
class MateriaisAdmin(admin.ModelAdmin):
    list_display = (
        "id_material",
        "nome",
        "cor_nbr",
        "exibir_amostra_cor",
        "pontos_por_kg",
    )
    search_fields = ("nome", "cor_nbr")

    @admin.display(description="Amostra de Cor")
    def exibir_amostra_cor(self, obj):
        if obj.codigo_hex:
            return format_html(
                '<span style="background-color: {}; padding: 3px 12px; border-radius: 3px; border: 1px solid #ccc; color: #fff; font-weight: bold; text-shadow: 1px 1px 1px #000;">{}</span>',
                obj.codigo_hex,
                obj.codigo_hex,
            )
        return "-"


class ItensColetaInline(admin.TabularInline):
    model = ItensColeta
    extra = 1
    autocomplete_fields = ("id_material",)


@admin.register(Coletas)
class ColetasAdmin(admin.ModelAdmin):
    list_display = (
        "id_coleta",
        "codigo_transacao",
        "id_usuario",
        "id_ecoponto",
        "total_pontos_gerados",
        "data_coleta",
    )
    list_filter = ("data_coleta", "id_ecoponto")
    search_fields = ("codigo_transacao", "id_usuario__nome", "id_ecoponto__nome")
    readonly_fields = ("id_coleta",)
    autocomplete_fields = ("id_usuario", "id_ecoponto")
    date_hierarchy = "data_coleta"
    inlines = [ItensColetaInline]


@admin.register(ItensColeta)
class ItensColetaAdmin(admin.ModelAdmin):
    list_display = ("id_item", "id_coleta", "id_material", "peso_kg", "pontos_ganhos")
    list_filter = ("id_material",)
    autocomplete_fields = ("id_coleta", "id_material")


@admin.register(Recompensas)
class RecompensasAdmin(admin.ModelAdmin):
    list_display = (
        "id_recompensa",
        "titulo",
        "custo_pontos",
        "estoque",
        "exibir_status",
    )
    list_filter = ("ativo",)
    search_fields = ("titulo", "descricao")

    @admin.display(description="Status")
    def exibir_status(self, obj):
        if obj.ativo == 1:
            return format_html(
                '<span style="color: green; font-weight: bold;">Ativo</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">Inativo</span>'
        )


@admin.register(Resgates)
class ResgatesAdmin(admin.ModelAdmin):
    list_display = (
        "id_resgate",
        "codigo_voucher",
        "id_usuario",
        "id_recompensa",
        "exibir_status",
        "data_resgate",
    )
    list_filter = ("status", "data_resgate")
    search_fields = ("codigo_voucher", "id_usuario__nome", "id_recompensa__titulo")
    readonly_fields = ("id_resgate",)
    autocomplete_fields = ("id_usuario", "id_recompensa")
    date_hierarchy = "data_resgate"

    @admin.display(description="Status")
    def exibir_status(self, obj):
        status_colors = {
            "pendente": "orange",
            "concluido": "green",
            "cancelado": "red",
        }
        color = status_colors.get(str(obj.status).lower(), "gray")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>', color, obj.status
        )


@admin.register(VwDashboardMetricas)
class VwDashboardMetricasAdmin(admin.ModelAdmin):
    list_display = (
        "total_usuarios",
        "total_kg_reciclados",
        "total_pontos_distribuidos",
        "total_resgates_concluidos",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
