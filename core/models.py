# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Coletas(models.Model):
    id_coleta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        "Usuarios", models.DO_NOTHING, db_column="id_usuario"
    )
    id_ecoponto = models.ForeignKey(
        "Ecopontos", models.DO_NOTHING, db_column="id_ecoponto"
    )
    codigo_transacao = models.CharField(unique=True, max_length=64)
    total_pontos_gerados = models.IntegerField()
    data_coleta = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "coletas"


class Ecopontos(models.Model):
    id_ecoponto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    endereco = models.CharField(max_length=200)
    ativo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ecopontos"


class ItensColeta(models.Model):
    id_item = models.AutoField(primary_key=True)
    id_coleta = models.ForeignKey(Coletas, models.DO_NOTHING, db_column="id_coleta")
    id_material = models.ForeignKey(
        "Materiais", models.DO_NOTHING, db_column="id_material"
    )
    peso_kg = models.DecimalField(max_digits=8, decimal_places=2)
    pontos_ganhos = models.IntegerField()
    qrcode_lote = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "itens_coleta"


class Materiais(models.Model):
    id_material = models.AutoField(primary_key=True)
    nome = models.CharField(unique=True, max_length=50)
    cor_nbr = models.CharField(max_length=20)
    codigo_hex = models.CharField(max_length=7)
    pontos_por_kg = models.IntegerField()

    class Meta:
        managed = False
        db_table = "materiais"


class Perfis(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    nome = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = "perfis"


class Recompensas(models.Model):
    id_recompensa = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    custo_pontos = models.IntegerField()
    estoque = models.IntegerField()
    ativo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "recompensas"


class Resgates(models.Model):
    id_resgate = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        "Usuarios", models.DO_NOTHING, db_column="id_usuario"
    )
    id_recompensa = models.ForeignKey(
        Recompensas, models.DO_NOTHING, db_column="id_recompensa"
    )
    pontos_gastos = models.IntegerField()
    codigo_voucher = models.CharField(unique=True, max_length=32)
    status = models.CharField(max_length=9, blank=True, null=True)
    data_resgate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "resgates"


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    id_perfil = models.ForeignKey(Perfis, models.DO_NOTHING, db_column="id_perfil")
    nome = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    cpf = models.CharField(unique=True, max_length=14)
    senha_hash = models.CharField(max_length=255)
    qrcode_token = models.CharField(unique=True, max_length=64)
    saldo_pontos = models.IntegerField(blank=True, null=True)
    criado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "usuarios"


class VwDashboardMetricas(models.Model):
    total_usuarios = models.BigIntegerField(primary_key=True)
    total_kg_reciclados = models.DecimalField(max_digits=30, decimal_places=2)
    total_pontos_distribuidos = models.DecimalField(max_digits=32, decimal_places=0)
    total_resgates_concluidos = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "vw_dashboard_metricas"
