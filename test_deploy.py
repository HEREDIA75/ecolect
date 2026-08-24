import sys
import requests

# Defina as URLs que deseja testar
URLS_PARA_TESTAR = {
    "Local": "http://127.0.0.1:8000",
    "Railway": "https://ecolect-production.up.railway.app",
}


def testar_ambiente(nome, base_url):
    print(f"\n--- Iniciando testes para: {nome} ({base_url}) ---")

    # 1. Teste do Painel Principal / Dashboard (Valida conexão com BD e VIEWs)
    try:
        res_dash = requests.get(f"{base_url}/", timeout=10)
        if res_dash.status_code == 200:
            print(f"[OK] Dashboard (GET /) - Status 200")
        else:
            print(f"[ERRO] Dashboard retornado status: {res_dash.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[FALHA DE CONEXÃO] Não foi possível conectar ao Dashboard: {e}")
        return

    # 2. Teste da rota de Login do Admin
    try:
        res_admin = requests.get(f"{base_url}/admin/login/", timeout=10)
        if res_admin.status_code == 200:
            print(f"[OK] Django Admin (GET /admin/login/) - Status 200")
        else:
            print(f"[AVISO] Admin retornado status: {res_admin.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha ao testar Django Admin: {e}")

    # 3. Teste de Arquivo Estático (CSS do Admin / WhiteNoise)
    try:
        res_static = requests.get(f"{base_url}/static/admin/css/base.css", timeout=10)
        if res_static.status_code == 200:
            print(f"[OK] Arquivos Estáticos / WhiteNoise - Status 200")
        else:
            print(
                f"[ERRO] Arquivos Estáticos com problemas. Status: {res_static.status_code}"
            )
            print("      Dica: Execute 'python manage.py collectstatic --noinput'")
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha ao testar Arquivos Estáticos: {e}")


if __name__ == "__main__":
    # Garante que a biblioteca requests está instalada
    try:
        import requests
    except ImportError:
        print("Instale a biblioteca 'requests' para rodar os testes:")
        print("pip install requests")
        sys.exit(1)

    print("=== SUÍTE DE TESTES AUTOMATIZADOS - ECOLECT ===")

    # Para testar apenas um ambiente específico, você pode passar como argumento no terminal:
    # python test_deploy.py local OU python test_deploy.py railway
    if len(sys.argv) > 1:
        alvo = sys.argv[1].lower()
        if alvo == "local":
            testar_ambiente("Local", URLS_PARA_TESTAR["Local"])
        elif alvo == "railway":
            testar_ambiente("Railway", URLS_PARA_TESTAR["Railway"])
        else:
            print("Opção inválida. Use 'local' ou 'railway'.")
    else:
        # Testa ambos os ambientes por padrão
        for nome, url in URLS_PARA_TESTAR.items():
            testar_ambiente(nome, url)
