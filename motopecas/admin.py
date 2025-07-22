from django.contrib import admin

from motopecas.models import Produto, VendaItem

# Register your models here.
admin.site.register(Produto)
admin.site.register(VendaItem)