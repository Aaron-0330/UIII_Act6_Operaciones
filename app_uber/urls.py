# app_uber/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # INICIO
    # ==========================================
    path('', views.inicio_uber, name='inicio_uber'),

    # ==========================================
    # USUARIO PASAJERO
    # ==========================================
    path('usuario_pasajero/agregar/', views.agregar_usuario_pasajero, name='agregar_usuario_pasajero'),
    path('usuario_pasajero/ver/', views.ver_usuario_pasajero, name='ver_usuario_pasajero'),
    path('usuario_pasajero/actualizar/<int:id_usuario>/', views.actualizar_usuario_pasajero, name='actualizar_usuario_pasajero'),
    path('usuario_pasajero/actualizar/realizar/<int:id_usuario>/', views.realizar_actualizacion_usuario_pasajero, name='realizar_actualizacion_usuario_pasajero'),
    path('usuario_pasajero/borrar/<int:id_usuario>/', views.borrar_usuario_pasajero, name='borrar_usuario_pasajero'),

    # ==========================================
    # CHOFER
    # ==========================================
    path('chofer/agregar/', views.agregar_chofer, name='agregar_chofer'),
    path('chofer/ver/', views.ver_chofer, name='ver_chofer'),
    path('chofer/actualizar/<int:id_chofer>/', views.actualizar_chofer, name='actualizar_chofer'),
    path('chofer/actualizar/realizar/<int:id_chofer>/', views.realizar_actualizacion_chofer, name='realizar_actualizacion_chofer'),
    path('chofer/borrar/<int:id_chofer>/', views.borrar_chofer, name='borrar_chofer'),
    
    # ==========================================
    # VIAJE
    # ==========================================
    path('viaje/agregar/', views.agregar_viaje, name='agregar_viaje'),
    path('viaje/ver/', views.ver_viaje, name='ver_viaje'),
    path('viaje/actualizar/<int:id_viaje>/', views.actualizar_viaje, name='actualizar_viaje'),
    path('viaje/actualizar/realizar/<int:id_viaje>/', views.realizar_actualizacion_viaje, name='realizar_actualizacion_viaje'),
    path('viaje/borrar/<int:id_viaje>/', views.borrar_viaje, name='borrar_viaje'),

    # ==========================================
    # VEHÍCULO (Nuevas)
    # ==========================================
    path('vehiculo/agregar/', views.agregar_vehiculo, name='agregar_vehiculo'),
    path('vehiculo/ver/', views.ver_vehiculo, name='ver_vehiculo'),
    path('vehiculo/actualizar/<int:id_vehiculo>/', views.actualizar_vehiculo, name='actualizar_vehiculo'),
    path('vehiculo/actualizar/realizar/<int:id_vehiculo>/', views.realizar_actualizacion_vehiculo, name='realizar_actualizacion_vehiculo'),
    path('vehiculo/borrar/<int:id_vehiculo>/', views.borrar_vehiculo, name='borrar_vehiculo'),

    # ==========================================
    # PAGOS (Nuevas)
    # ==========================================
    path('pagos/agregar/', views.agregar_pago, name='agregar_pago'),
    path('pagos/ver/', views.ver_pagos, name='ver_pagos'),
    path('pagos/actualizar/<int:id_pago>/', views.actualizar_pago, name='actualizar_pago'),
    path('pagos/actualizar/realizar/<int:id_pago>/', views.realizar_actualizacion_pago, name='realizar_actualizacion_pago'),
    path('pagos/borrar/<int:id_pago>/', views.borrar_pago, name='borrar_pago'),

    # ==========================================
    # TARJETAS (Nuevas)
    # ==========================================
    path('tarjetas/agregar/', views.agregar_tarjeta, name='agregar_tarjeta'),
    path('tarjetas/ver/', views.ver_tarjetas, name='ver_tarjetas'),
    path('tarjetas/actualizar/<int:id_tarjeta>/', views.actualizar_tarjeta, name='actualizar_tarjeta'),
    path('tarjetas/actualizar/realizar/<int:id_tarjeta>/', views.realizar_actualizacion_tarjeta, name='realizar_actualizacion_tarjeta'),
    path('tarjetas/borrar/<int:id_tarjeta>/', views.borrar_tarjeta, name='borrar_tarjeta'),

    # ==========================================
    # COMENTARIOS (Nuevas)
    # ==========================================
    path('comentarios/agregar/', views.agregar_comentario, name='agregar_comentario'),
    path('comentarios/ver/', views.ver_comentarios, name='ver_comentarios'),
    path('comentarios/actualizar/<int:id_comentario>/', views.actualizar_comentario, name='actualizar_comentario'),
    path('comentarios/actualizar/realizar/<int:id_comentario>/', views.realizar_actualizacion_comentario, name='realizar_actualizacion_comentario'),
    path('comentarios/borrar/<int:id_comentario>/', views.borrar_comentario, name='borrar_comentario'),

    # ==========================================
    # CUENTA DUEÑO (Nuevas)
    # ==========================================
    path('cuenta_dueno/agregar/', views.agregar_cuenta_dueno, name='agregar_cuenta_dueno'),
    path('cuenta_dueno/ver/', views.ver_cuentas_dueno, name='ver_cuentas_dueno'),
    path('cuenta_dueno/actualizar/<int:id_dueno>/', views.actualizar_cuenta_dueno, name='actualizar_cuenta_dueno'),
    path('cuenta_dueno/actualizar/realizar/<int:id_dueno>/', views.realizar_actualizacion_cuenta_dueno, name='realizar_actualizacion_cuenta_dueno'),
    path('cuenta_dueno/borrar/<int:id_dueno>/', views.borrar_cuenta_dueno, name='borrar_cuenta_dueno'),
]