import os
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Executa testes automatizados de integridade no ambiente do Railway"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("=== HEALTHCHECK AUTOMATIZADO DE AMBIENTE ==="))

        # 1. Teste do Banco de Dados e VIEW
        self.stdout.write("\n1. Testando conexão com o Banco de Dados e VIEW de Métricas...")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM vw_dashboard_metricas LIMIT 1;")
                row = cursor.fetchone()
                self.stdout.write(
                    self.style.SUCCESS(f"  [OK] Conexão ativa ({connection.vendor.upper()}). VIEW 'vw_dashboard_metricas' legível.")
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"  [ERRO] Falha ao consultar a VIEW/Banco: {e}")
            )

        # 2. Teste de Arquivos Estáticos (WhiteNoise / Staticfiles)
        self.stdout.write("\n2. Testando arquivos estáticos...")
        static_root = os.getenv("STATIC_ROOT", "staticfiles")
        if os.path.exists(static_root):
            self.stdout.write(
                self.style.SUCCESS(f"  [OK] Diretório de estáticos encontrado em: {static_root}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"  [AVISO] Diretório '{static_root}' não encontrado. Certifique-se de rodar 'collectstatic'."
                )
            )

        # 3. Teste das Variáveis de Ambiente Críticas
        self.stdout.write("\n3. Validando variáveis de ambiente...")
        debug_state = os.getenv("DEBUG", "False")
        allowed_hosts = os.getenv("ALLOWED_HOSTS", "Não definido")
        db_url_present = "Sim" if os.getenv("DATABASE_URL") or os.getenv("DB_NAME") else "Não"

        self.stdout.write(f"  - DEBUG: {debug_state}")
        self.stdout.write(f"  - ALLOWED_HOSTS: {allowed_hosts}")
        self.stdout.write(f"  - Banco Configurado: {db_url_present}")

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== FIM DOS TESTES ==="))
