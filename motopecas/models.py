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
