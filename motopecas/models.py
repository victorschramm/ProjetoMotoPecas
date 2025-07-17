from django.db import models
from .enum import Garantia, FormaPagamento, Unidades
from django.contrib.auth.models import AbstractUser

class Fornecedor(models.Model):
    cnpj = models.CharField(max_length=14)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=12)
    email = models.EmailField(max_length=100)

class Produto(models.Model):
    descricao = models.CharField(max_length=200)
    marca = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()
    unidade = models.CharField(max_length=50 ,choices=Unidades.choices, default=Unidades.UNIDADE)

class Usuario(AbstractUser):
    telefone = models.CharField(max_length=15)
    funcao = models.CharField(max_length=50)

class Cliente(models.Model):
   cpf = models.CharField(max_length=11 , null=False, unique=True)
   nome = models.CharField(max_length=100)             
   telefone = models.CharField(max_length=15)          
       
class Veiculo(models.Model):
   proprietario = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
   placa = models.CharField(max_length=7)
   marca = models.CharField(max_length=50)
   modelo = models.CharField(max_length=100)

class Servico(models.Model):
    descricao = models.CharField(max_length=150)
    garantia = models.CharField(max_length=3, choices=Garantia.choices, default=Garantia.G7)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

class StatusPagamento(models.TextChoices):
    REALIZADO = 'REA', 'Realizado'
    PENDENTE = 'PEN', 'Pendente'
    PARCIALMENTE_PENDENTE = 'PPEN', 'Parcialmente Pendente'

class Pagamento(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    formaPagamento = models.CharField(max_length=4, choices=FormaPagamento.choices, default=FormaPagamento.DINHEIRO)
    statusPagamento = models.CharField(max_length=4, choices=StatusPagamento.choices, default=StatusPagamento.REALIZADO)

class VendaServico(models.Model):
    data = models.DateField(auto_now_add=True)
    servico = models.ForeignKey(Servico, on_delete=models.RESTRICT)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.RESTRICT)
    usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    pagamento = models.ForeignKey(Pagamento, related_name="VendaServico", on_delete=models.RESTRICT)

class HistoricoPrecoServico(models.Model):
    dataInicio = models.DateField(auto_now_add=True)
    dataFim = models.DateField()
    precoCobrado = models.DecimalField(max_digits=10, decimal_places=2)
    servico = models.ForeignKey(Servico, related_name="HistoricoPrecoServico", on_delete=models.RESTRICT)

class HistoricoPrecoProduto(models.Model):
    dataInicio = models.DateField(auto_now_add=True)
    dataFim = models.DateField()
    precoDeCompra = models.DecimalField(max_digits=10, decimal_places=2)
    precoDeVenda = models.DecimalField(max_digits=10, decimal_places=2)
    produto = models.ForeignKey(Produto, related_name="HistoricoPrecoProduto", on_delete=models.RESTRICT)

class Pedido(models.Model):
    data =  models.DateField(auto_now_add=True)
    valor =  models.DecimalField(max_digits=10, decimal_places=2)
    fornecedor = models.ForeignKey(Fornecedor, related_name="Pedido", on_delete=models.RESTRICT)

class PedidoProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.RESTRICT, related_name='pedido_produtos')
    pedido = models.ForeignKey(Pedido, on_delete=models.RESTRICT, related_name='pedido_produtos')
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

class VendaProduto(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT,related_name="Cliente")
    funcionario = models.ForeignKey(Usuario, on_delete=models.RESTRICT, related_name="Funcionario")
    pagamento = models.ForeignKey(Pagamento, on_delete=models.RESTRICT, null=True, blank=True, related_name="Pagamento")
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2)

class VendaItem(models.Model):
    venda = models.ForeignKey(VendaProduto, on_delete=models.RESTRICT,related_name="Venda")
    produto = models.ForeignKey(Produto, on_delete=models.RESTRICT, related_name="Produto")
    quantidade_vendida = models.PositiveIntegerField()
    precoVenda = models.DecimalField(max_digits=10, decimal_places=2)
