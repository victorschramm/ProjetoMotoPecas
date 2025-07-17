from django.db import models
# Enumeração de opções de garantia para serviços/produtos
class Garantia(models.TextChoices):
    G0 = '0d', '0 dias'
    G7 = '7d', '7 dias'     
    G14 = '14d', '14 dias'  
    G30 = '30d', '30 dias'  
    G60 = '60d', '60 dias'  
    G90 = '90d', '90 dias'  

# Enumeração das formas de pagamento aceitas
class FormaPagamento(models.TextChoices):
    PIX = 'PIX', 'Pix'       
    CREDITO = 'CRED', 'Cartão de Crédito'  
    DEBITO = 'DEB', 'Cartão de Débito'    
    DINHEIRO = 'DIN', 'Dinheiro' 
    FIADO = 'FIA', 'Fiado' 

# Enumeração de unidades de medida para produtos
class Unidades(models.TextChoices):
    UNIDADE = 'UN', 'Unidade'
    CAIXA = 'CX', 'Caixa'    
    LITRO = 'LT', 'Litro'    
    METRO = 'MT', 'Metro'    
    PACOTE = 'PC', 'Pacote'  
    JOGO = 'JG', 'Jogo'      
    FRASCO = 'FR', 'Frasco'  
    KILO = 'KG', 'Quilo'     


# Status possíveis para o pagamento
class StatusPagamento(models.TextChoices):
    REALIZADO = 'REA', 'Realizado'
    PENDENTE = 'PEN', 'Pendente'
    PARCIALMENTE_PENDENTE = 'PPEN', 'Parcialmente Pendente'