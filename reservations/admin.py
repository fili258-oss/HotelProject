#from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Promocion, Reserva, ReservaPromociones, Factura, ItemFactura, Pago

admin.site.register(Promocion)
admin.site.register(Reserva)
admin.site.register(ReservaPromociones)
admin.site.register(Factura)
admin.site.register(ItemFactura)
admin.site.register(Pago)