from django.db import models
from django.contrib.auth.models import AbstractUser

class Fornecedor(models.Model):
    cnpj = models.CharField(max_length=14)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=12)
    email = models.CharField(max_length=100)

class Produto(models.Model):
    descricao = models.CharField(max_length=200)
    marca = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    unidade =  models.CharField(max_length=10)

class Usuario(AbstractUser):
    telefone = models.CharField(max_length=15)
    funcao = models.CharField(max_length=50)

class Cliente(models.Model):
   cpf = models.CharField(max_length=11 , null=False, unique=True)
   nome = models.CharField(max_length=100)             
   telefone = models.CharField(max_length=15)          
       
class Veiculo(models.Model):
   proprietario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
   placa = models.CharField(max_length=7)
   marca = models.CharField(max_length=50)
   modelo = models.CharField(max_length=100)

class Garantia(models.TextChoices):
    G0 = '0d', '0 dias'
    G7 = '7d', '7 dias'
    G14 = '14d', '14 dias'
    G30 = '30d', '30 dias'
    G60 = '60d', '60 dias'
    G90 = '90d', '90 dias'

class FormaPagamento(models.TextChoices):
    PIX = 'PIX', 'Pix'
    CREDITO = 'CRED', 'Cartão de Crédito'
    DEBITO = 'DEB', 'Cartão de Débito'
    DINHEIRO = 'DIN', 'Dinheiro'
    FIADO = 'FIA', 'Fiado'

class Servico(models.Model):
    descricao = models.CharField(max_length=150)
    garantia = models.CharField(max_length=3, choices=Garantia.choices, default=Garantia.G7)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

class Pagamento(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=4, choices=FormaPagamento.choices, default=FormaPagamento.PIX)
