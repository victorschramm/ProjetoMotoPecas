from django.db import models
from .enum import Garantia, FormaPagamento, Unidades
from django.contrib.auth.models import AbstractUser

# Modelo que representa os dados do fornecedor
class Fornecedor(models.Model):
    cnpj = models.CharField(max_length=14)  # CNPJ do fornecedor
    nome = models.CharField(max_length=100)  # Nome do fornecedor
    telefone = models.CharField(max_length=12)  # Telefone de contato
    email = models.EmailField(max_length=100)  # E-mail de contato

# Modelo de produtos cadastrados
class Produto(models.Model):
    descricao = models.CharField(max_length=200)  # Descrição do produto
    marca = models.CharField(max_length=100)  # Marca do produto
    quantidade = models.PositiveIntegerField()  # Quantidade disponível
    unidade = models.CharField(max_length=50, choices=Unidades.choices, default=Unidades.UNIDADE)  # Unidade de medida

# Modelo de usuário do sistema com informações adicionais
class Usuario(AbstractUser):
    telefone = models.CharField(max_length=15)  # Telefone do usuário
    funcao = models.CharField(max_length=50)  # Função/cargo do usuário

# Modelo que representa os clientes
class Cliente(models.Model):
    cpf = models.CharField(max_length=11, null=False, unique=True)  # CPF do cliente
    nome = models.CharField(max_length=100)  # Nome do cliente
    telefone = models.CharField(max_length=15)  # Telefone de contato

# Veículo vinculado a um cliente
class Veiculo(models.Model):
    proprietario = models.ForeignKey(Cliente, on_delete=models.RESTRICT)  # Dono do veículo
    placa = models.CharField(max_length=7)  # Placa do veículo
    marca = models.CharField(max_length=50)  # Marca do veículo
    modelo = models.CharField(max_length=100)  # Modelo do veículo

# Serviço disponível no sistema
class Servico(models.Model):
    descricao = models.CharField(max_length=150)  # Descrição do serviço
    garantia = models.CharField(max_length=3, choices=Garantia.choices, default=Garantia.G7)  # Garantia oferecida
    preco = models.DecimalField(max_digits=10, decimal_places=2)  # Preço do serviço

# Status possíveis para o pagamento
class StatusPagamento(models.TextChoices):
    REALIZADO = 'REA', 'Realizado'
    PENDENTE = 'PEN', 'Pendente'
    PARCIALMENTE_PENDENTE = 'PPEN', 'Parcialmente Pendente'

# Registro de pagamentos
class Pagamento(models.Model):
    data = models.DateTimeField(auto_now_add=True)  # Data do pagamento
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor pago
    formaPagamento = models.CharField(max_length=4, choices=FormaPagamento.choices, default=FormaPagamento.DINHEIRO)  # Forma de pagamento
    statusPagamento = models.CharField(max_length=4, choices=StatusPagamento.choices, default=StatusPagamento.REALIZADO)  # Status do pagamento

# Registro de venda de serviços
class VendaServico(models.Model):
    data = models.DateField(auto_now_add=True)  # Data da venda
    servico = models.ForeignKey(Servico, on_delete=models.RESTRICT)  # Serviço vendido
    veiculo = models.ForeignKey(Veiculo, on_delete=models.RESTRICT)  # Veículo atendido
    usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)  # Funcionário que realizou o serviço
    pagamento = models.ForeignKey(Pagamento, related_name="VendaServico", on_delete=models.RESTRICT)  # Pagamento associado

# Histórico de preços praticados para serviços
class HistoricoPrecoServico(models.Model):
    dataInicio = models.DateField(auto_now_add=True)  # Início do período
    dataFim = models.DateField()  # Fim do período
    precoCobrado = models.DecimalField(max_digits=10, decimal_places=2)  # Preço cobrado no período
    servico = models.ForeignKey(Servico, related_name="HistoricoPrecoServico", on_delete=models.RESTRICT)  # Serviço relacionado

# Histórico de preços praticados para produtos
class HistoricoPrecoProduto(models.Model):
    dataInicio = models.DateField(auto_now_add=True)  # Início do período
    dataFim = models.DateField()  # Fim do período
    precoDeCompra = models.DecimalField(max_digits=10, decimal_places=2)  # Preço de compra no período
    precoDeVenda = models.DecimalField(max_digits=10, decimal_places=2)  # Preço de venda no período
    produto = models.ForeignKey(Produto, related_name="HistoricoPrecoProduto", on_delete=models.RESTRICT)  # Produto relacionado

# Registro de compras feitas ao fornecedor
class Pedido(models.Model):
    data = models.DateField(auto_now_add=True)  # Data do pedido
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2)  # Valor total da compra
    fornecedor = models.ForeignKey(Fornecedor, related_name="Pedido", on_delete=models.RESTRICT)  # Fornecedor responsável

# Produtos incluídos em um pedido
class PedidoProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.RESTRICT, related_name='pedido_produtos')  # Produto comprado
    pedido = models.ForeignKey(Pedido, on_delete=models.RESTRICT, related_name='pedido_produtos')  # Pedido referente
    quantidade = models.PositiveIntegerField()  # Quantidade adquirida
    preco = models.DecimalField(max_digits=10, decimal_places=2)  # Preço unitário no pedido

# Registro de venda de produtos
class VendaProduto(models.Model):
    data = models.DateTimeField(auto_now_add=True)  # Data da venda
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, related_name="Cliente")  # Cliente comprador
    funcionario = models.ForeignKey(Usuario, on_delete=models.RESTRICT, related_name="Funcionario")  # Funcionário responsável
    pagamento = models.ForeignKey(Pagamento, on_delete=models.RESTRICT, null=True, blank=True, related_name="Pagamento")  # Pagamento vinculado
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2)  # Valor total da venda

# Produtos vendidos em cada venda
class VendaItem(models.Model):
    venda = models.ForeignKey(VendaProduto, on_delete=models.RESTRICT, related_name="Venda")  # Venda à qual pertence
    produto = models.ForeignKey(Produto, on_delete=models.RESTRICT, related_name="Produto")  # Produto vendido
    quantidade = models.PositiveIntegerField()  # Quantidade vendida
    precoUnitario = models.DecimalField(max_digits=10, decimal_places=2)  # Preço por unidade
