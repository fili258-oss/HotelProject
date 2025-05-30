from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('facturas/', views.listar_facturas_view, name='listar_facturas'),
    path('facturas/<int:factura_id>/', views.detalle_factura_view, name='detalle_factura'),
    path('facturas/<int:factura_id>/pago/', views.realizar_pago_view, name='realizar_pago'),
    path('promociones/crear/', views.crear_promocion_view, name='crear_promocion'),
    path('reservas/crear/', views.crear_reserva_view, name='crear_reserva'),
    path('promociones/activas/', views.listar_promociones_activas_view, name='listar_promociones_activas'),
    path('hoteles/<int:hotel_id>/ingresos/', views.calcular_ingreso_hotel_view, name='calcular_ingreso_hotel'),
    path('hoteles/<int:hotel_id>/ocupacion/', views.vista_ocupacion_actual_view, name='vista_ocupacion_actual'),
    path('ajustes/', views.ajustes_admin_view, name='ajustes_admin'),
]