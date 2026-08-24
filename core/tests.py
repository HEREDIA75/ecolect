from django.test import TestCase
from core.models import Perfis, Usuarios, Ecopontos, Materiais, Coletas, ItensColeta


class EcoLlectModelsTestCase(TestCase):

    def setUp(self):
        self.perfil = Perfis.objects.create(nome="Cidadão")
        self.usuario = Usuarios.objects.create(
            id_perfil=self.perfil,
            nome="Carlos Silva",
            email="carlos@exemplo.com",
            cpf="123.456.789-00",
            senha_hash="pbkdf2_sha256$test_hash",
            qrcode_token="token_teste_123",
            saldo_pontos=100,
        )
        self.ecoponto = Ecopontos.objects.create(
            nome="Ecoponto Central",
            latitude=-23.79,
            longitude=-45.40,
            cidade="São Sebastião",
            bairro="Centro",
            endereco="Rua Principal, 100",
            ativo=True,
        )
        self.material = Materiais.objects.create(
            nome="Plástico (PET)",
            cor_nbr="Vermelho",
            codigo_hex="#FF0000",
            pontos_por_kg=50,
        )

    def test_criacao_usuario(self):
        self.assertEqual(self.usuario.saldo_pontos, 100)
        self.assertEqual(str(self.usuario), "Carlos Silva (123.456.789-00)")

    def test_registro_coleta_e_itens(self):
        coleta = Coletas.objects.create(
            usuario=self.usuario,
            ecoponto=self.ecoponto,
            codigo_transacao="TX-999888777",
            total_pontos_gerados=100,
        )
        item = ItensColeta.objects.create(
            coleta=coleta, material=self.material, peso_kg=2.00, pontos_ganhos=100
        )
        self.assertEqual(coleta.itens.count(), 1)
        self.assertEqual(item.pontos_ganhos, 100)
