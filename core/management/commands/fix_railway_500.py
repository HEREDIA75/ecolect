import os
from django.core.management.base import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    help = "Detecta e corrige automaticamente causas comuns de erro 500 no Railway."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("=== AUTODIAG NÓSTICO E AUTO-REPARO ECOLECT ==="))
        
        # 1. Testar se a VIEW existe e se aceita SELECT
        self.stdout.write("\n[1/3] Verificando integridade da VIEW 'vw_dashboard_metricas'...")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM vw_dashboard_metricas;")
                colunas = [col[0] for col in cursor.description]
                dados = cursor.fetchall()
                self.stdout.write(self.style.SUCCESS(f"  ✓ VIEW operacional. Colunas encontradas: {colunas}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Erro na VIEW: {e}"))
            self.stdout.write("  -> Recriando VIEW padrão de contingência...")
            self.reconstruir_view()

        # 2. Testar se o banco MySQL precisa de re-aplicação de migrações
        self.stdout.write("\n[2/3] Verificando sincronia das Migrações...")
        try:
            from django.core.management import call_command
            call_command("migrate", interactive=False)
            self.stdout.write(self.style.SUCCESS("  ✓ Migrações aplicadas com sucesso."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Erro ao migrar: {e}"))

        # 3. Testar Renderização Interna da View/Template da Home
        self.stdout.write("\n[3/3] Simulando requisição na Rota Principal ('/')...")
        try:
            from django.test import RequestFactory
            from setup.urls import urlpatterns
            from django.urls import resolve

            factory = RequestFactory()
            request = factory.get('/')
            match = resolve('/')
            response = match.func(request)
            
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS("  ✓ Rota principal renderizada sem erros internos (Status 200)."))
            else:
                self.stdout.write(self.style.WARNING(f"  ! Rota retornou Status {response.status_code}."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ ERRO ENCONTRADO NA RENDERIZAÇÃO: {e}"))
            self.stdout.write("  -> Verifique se há variáveis não tratadas ou divisão por zero na View/Template.")

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== DIAGNÓSTICO CONCLUÍDO ==="))

    def reconstruir_view(self):
        query_sql = """
        CREATE OR REPLACE VIEW vw_dashboard_metricas AS
        SELECT 
            1 AS id,
            0 AS total_ecopontos,
            0 AS total_coletas,
            0 AS total_usuarios,
            0.0 AS total_kg_reciclados,
            0 AS total_pontos_distribuidos,
            0 AS total_resgates_concluidos;
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("DROP VIEW IF EXISTS vw_dashboard_metricas;")
                cursor.execute(query_sql)
            self.stdout.write(self.style.SUCCESS("  ✓ VIEW 'vw_dashboard_metricas' recriada com sucesso!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Falha ao recriar VIEW: {e}"))
