# app_uber/views.py
from django.shortcuts import render, redirect, get_object_or_404
# Importamos todos los modelos. Asumo que "Viaje" es el nombre de tu clase (singular)
from .models import UsuarioPasajero, Chofer, Viaje, Vehiculo, Pagos, Tarjetas, Comentario, CuentaDueno
from datetime import date

def inicio_uber(request):
    return render(request, 'inicio.html')

# ========================================================
# 1. USUARIO PASAJERO (Tus campos + Relación Chofer Pref)
# ========================================================

def agregar_usuario_pasajero(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST['telefono']
        direccion = request.POST['direccion']
        genero = request.POST['genero']
        ciudad = request.POST['ciudad']
        
        # Relación opcional con Chofer Preferido
        chofer_preferido_id = request.POST.get('chofer_preferido')
        chofer_preferido = None
        if chofer_preferido_id:
            try:
                chofer_preferido = Chofer.objects.get(pk=chofer_preferido_id)
            except Chofer.DoesNotExist:
                pass 

        UsuarioPasajero.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono,
            direccion=direccion,
            fecha_registro=date.today(),
            genero=genero,
            ciudad=ciudad,
            chofer_preferido=chofer_preferido
        )
        return redirect('ver_usuario_pasajero')
    
    choferes = Chofer.objects.all()
    return render(request, 'usuario_pasajero/agregar_usuario_pasajero.html', {'choferes': choferes})

def ver_usuario_pasajero(request):
    pasajeros = UsuarioPasajero.objects.all()
    return render(request, 'usuario_pasajero/ver_usuario_pasajero.html', {'pasajeros': pasajeros})

def actualizar_usuario_pasajero(request, id_usuario):
    pasajero = get_object_or_404(UsuarioPasajero, pk=id_usuario)
    choferes = Chofer.objects.all()
    return render(request, 'usuario_pasajero/actualizar_usuario_pasajero.html', {'pasajero': pasajero, 'choferes': choferes})

def realizar_actualizacion_usuario_pasajero(request, id_usuario):
    if request.method == 'POST':
        pasajero = get_object_or_404(UsuarioPasajero, pk=id_usuario)
        pasajero.nombre = request.POST['nombre']
        pasajero.email = request.POST['email']
        pasajero.telefono = request.POST['telefono']
        pasajero.direccion = request.POST['direccion']
        pasajero.genero = request.POST['genero']
        pasajero.ciudad = request.POST['ciudad']
        
        chofer_preferido_id = request.POST.get('chofer_preferido')
        if chofer_preferido_id:
            pasajero.chofer_preferido = get_object_or_404(Chofer, pk=chofer_preferido_id)
        else:
            pasajero.chofer_preferido = None
            
        pasajero.save()
        return redirect('ver_usuario_pasajero')
    return redirect('ver_usuario_pasajero')

def borrar_usuario_pasajero(request, id_usuario):
    pasajero = get_object_or_404(UsuarioPasajero, pk=id_usuario)
    if request.method == 'POST':
        pasajero.delete()
        return redirect('ver_usuario_pasajero')
    return render(request, 'usuario_pasajero/borrar_usuario_pasajero.html', {'pasajero': pasajero})


# ========================================================
# 2. CHOFER (Tus campos)
# ========================================================

def agregar_chofer(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        licencia = request.POST['licencia']
        telefono = request.POST['telefono']
        direccion = request.POST['direccion']
        email = request.POST['email']
        edad = request.POST['edad']
        fecha_ingreso = request.POST['fecha_ingreso']
        
        Chofer.objects.create(
            nombre=nombre,
            licencia=licencia,
            telefono=telefono,
            direccion=direccion,
            email=email,
            edad=edad,
            fecha_ingreso=fecha_ingreso
        )
        return redirect('ver_chofer')
    return render(request, 'chofer/agregar_chofer.html')

def ver_chofer(request):
    choferes = Chofer.objects.all()
    return render(request, 'chofer/ver_chofer.html', {'choferes': choferes})

def actualizar_chofer(request, id_chofer):
    chofer = get_object_or_404(Chofer, pk=id_chofer)
    return render(request, 'chofer/actualizar_chofer.html', {'chofer': chofer})

def realizar_actualizacion_chofer(request, id_chofer):
    if request.method == 'POST':
        chofer = get_object_or_404(Chofer, pk=id_chofer)
        chofer.nombre = request.POST['nombre']
        chofer.licencia = request.POST['licencia']
        chofer.telefono = request.POST['telefono']
        chofer.direccion = request.POST['direccion']
        chofer.email = request.POST['email']
        chofer.edad = request.POST['edad']
        chofer.fecha_ingreso = request.POST['fecha_ingreso']
        chofer.save()
        return redirect('ver_chofer')
    return redirect('ver_chofer')

def borrar_chofer(request, id_chofer):
    chofer = get_object_or_404(Chofer, pk=id_chofer)
    if request.method == 'POST':
        chofer.delete()
        return redirect('ver_chofer')
    return render(request, 'chofer/borrar_chofer.html', {'chofer': chofer})


# ========================================================
# 3. VIAJE (Tus campos + Pasajeros Many-to-Many + Chofer)
# ========================================================

def agregar_viaje(request):
    if request.method == 'POST':
        destino = request.POST['destino']
        fecha = request.POST['fecha']
        hora_salida = request.POST['hora_salida']
        duracion = request.POST['duracion']
        costo = request.POST['costo']
        estatus = request.POST['estatus']
        chofer_id = request.POST['chofer']
        pasajeros_ids = request.POST.getlist('pasajeros')

        chofer = get_object_or_404(Chofer, pk=chofer_id)
        
        viaje = Viaje.objects.create(
            destino=destino,
            fecha=fecha,
            hora_salida=hora_salida,
            duracion=duracion,
            costo=costo,
            estatus=estatus,
            chofer=chofer
        )
        
        # Relación Many-to-Many con pasajeros
        for pasajero_id in pasajeros_ids:
            pasajero = get_object_or_404(UsuarioPasajero, pk=pasajero_id)
            viaje.pasajeros.add(pasajero)
            
        return redirect('ver_viaje')
    
    choferes = Chofer.objects.all()
    pasajeros = UsuarioPasajero.objects.all()
    return render(request, 'viaje/agregar_viaje.html', {'choferes': choferes, 'pasajeros': pasajeros})

def ver_viaje(request):
    viajes = Viaje.objects.all()
    return render(request, 'viaje/ver_viaje.html', {'viajes': viajes})

def actualizar_viaje(request, id_viaje):
    viaje = get_object_or_404(Viaje, pk=id_viaje)
    choferes = Chofer.objects.all()
    pasajeros_disponibles = UsuarioPasajero.objects.all()
    pasajeros_actuales_ids = [p.pk for p in viaje.pasajeros.all()]

    return render(request, 'viaje/actualizar_viaje.html', {
        'viaje': viaje,
        'choferes': choferes,
        'pasajeros_disponibles': pasajeros_disponibles,
        'pasajeros_actuales_ids': pasajeros_actuales_ids,
    })

def realizar_actualizacion_viaje(request, id_viaje):
    if request.method == 'POST':
        viaje = get_object_or_404(Viaje, pk=id_viaje)
        
        viaje.destino = request.POST['destino']
        viaje.fecha = request.POST['fecha']
        viaje.hora_salida = request.POST['hora_salida']
        viaje.duracion = request.POST['duracion']
        viaje.costo = request.POST['costo']
        viaje.estatus = request.POST['estatus']
        
        chofer_id = request.POST['chofer']
        viaje.chofer = get_object_or_404(Chofer, pk=chofer_id)
        viaje.save()
        
        pasajeros_ids = request.POST.getlist('pasajeros')
        viaje.pasajeros.set(pasajeros_ids)
        
        return redirect('ver_viaje')
    return redirect('ver_viaje')

def borrar_viaje(request, id_viaje):
    viaje = get_object_or_404(Viaje, pk=id_viaje)
    if request.method == 'POST':
        viaje.delete()
        return redirect('ver_viaje')
    return render(request, 'viaje/borrar_viaje.html', {'viaje': viaje})


# ========================================================
# 4. VEHÍCULO (Vinculado a Chofer)
# ========================================================

def agregar_vehiculo(request):
    if request.method == 'POST':
        # Relación con Chofer (del diagrama)
        chofer_id = request.POST['chofer']
        marca_carro = request.POST['marca_carro']
        modelo_carro = request.POST['modelo_carro']
        matricula = request.POST['matricula']
        tipo_carro = request.POST['tipo_carro']

        chofer = get_object_or_404(Chofer, pk=chofer_id)

        Vehiculo.objects.create(
            chofer=chofer,
            marca_carro=marca_carro,
            modelo_carro=modelo_carro,
            matricula=matricula,
            tipo_carro=tipo_carro
        )
        return redirect('ver_vehiculo')

    choferes = Chofer.objects.all()
    return render(request, 'vehiculo/agregar_vehiculo.html', {'choferes': choferes})

def ver_vehiculo(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculo/ver_vehiculo.html', {'vehiculos': vehiculos})

def actualizar_vehiculo(request, id_vehiculo):
    vehiculo = get_object_or_404(Vehiculo, pk=id_vehiculo)
    choferes = Chofer.objects.all()
    return render(request, 'vehiculo/actualizar_vehiculo.html', {'vehiculo': vehiculo, 'choferes': choferes})

def realizar_actualizacion_vehiculo(request, id_vehiculo):
    if request.method == 'POST':
        vehiculo = get_object_or_404(Vehiculo, pk=id_vehiculo)
        
        vehiculo.chofer = get_object_or_404(Chofer, pk=request.POST['chofer'])
        vehiculo.marca_carro = request.POST['marca_carro']
        vehiculo.modelo_carro = request.POST['modelo_carro']
        vehiculo.matricula = request.POST['matricula']
        vehiculo.tipo_carro = request.POST['tipo_carro']
        vehiculo.save()
        return redirect('ver_vehiculo')
    return redirect('ver_vehiculo')

def borrar_vehiculo(request, id_vehiculo):
    vehiculo = get_object_or_404(Vehiculo, pk=id_vehiculo)
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('ver_vehiculo')
    return render(request, 'vehiculo/borrar_vehiculo.html', {'vehiculo': vehiculo})


# ========================================================
# 5. TARJETAS (Vinculado a UsuarioPasajero)
# ========================================================

def agregar_tarjeta(request):
    if request.method == 'POST':
        usuario_id = request.POST['usuario']
        numero_tarjeta = request.POST['numero_tarjeta']
        tipo_tarjeta = request.POST['tipo_tarjeta']
        fecha_vencimiento = request.POST['fecha_vencimiento']
        cv = request.POST['cv']

        usuario = get_object_or_404(UsuarioPasajero, pk=usuario_id)

        Tarjetas.objects.create(
            usuario=usuario,
            numero_tarjeta=numero_tarjeta,
            tipo_tarjeta=tipo_tarjeta,
            fecha_vencimiento=fecha_vencimiento,
            cv=cv
        )
        return redirect('ver_tarjetas')

    usuarios = UsuarioPasajero.objects.all()
    return render(request, 'tarjetas/agregar_tarjeta.html', {'usuarios': usuarios})

def ver_tarjetas(request):
    tarjetas = Tarjetas.objects.all()
    return render(request, 'tarjetas/ver_tarjetas.html', {'tarjetas': tarjetas})

def actualizar_tarjeta(request, id_tarjeta):
    tarjeta = get_object_or_404(Tarjetas, pk=id_tarjeta)
    usuarios = UsuarioPasajero.objects.all()
    return render(request, 'tarjetas/actualizar_tarjeta.html', {'tarjeta': tarjeta, 'usuarios': usuarios})

def realizar_actualizacion_tarjeta(request, id_tarjeta):
    if request.method == 'POST':
        tarjeta = get_object_or_404(Tarjetas, pk=id_tarjeta)
        
        tarjeta.usuario = get_object_or_404(UsuarioPasajero, pk=request.POST['usuario'])
        tarjeta.numero_tarjeta = request.POST['numero_tarjeta']
        tarjeta.tipo_tarjeta = request.POST['tipo_tarjeta']
        tarjeta.fecha_vencimiento = request.POST['fecha_vencimiento']
        tarjeta.cv = request.POST['cv']
        tarjeta.save()
        return redirect('ver_tarjetas')
    return redirect('ver_tarjetas')

def borrar_tarjeta(request, id_tarjeta):
    tarjeta = get_object_or_404(Tarjetas, pk=id_tarjeta)
    if request.method == 'POST':
        tarjeta.delete()
        return redirect('ver_tarjetas')
    return render(request, 'tarjetas/borrar_tarjeta.html', {'tarjeta': tarjeta})


# ========================================================
# 6. COMENTARIOS (Vinculado a Chofer y Viaje)
# ========================================================

def agregar_comentario(request):
    if request.method == 'POST':
        chofer_id = request.POST['chofer']
        viaje_id = request.POST['viaje']
        comentario_texto = request.POST['comentario']
        num_resena = request.POST.get('num_resena', 0)

        chofer = get_object_or_404(Chofer, pk=chofer_id)
        viaje = get_object_or_404(Viaje, pk=viaje_id)

        Comentario.objects.create(
            chofer=chofer,
            viaje=viaje,
            comentario=comentario_texto,
            num_resena=num_resena
        )
        return redirect('ver_comentarios')

    choferes = Chofer.objects.all()
    viajes = Viaje.objects.all()
    return render(request, 'comentarios/agregar_comentario.html', {'choferes': choferes, 'viajes': viajes})

def ver_comentarios(request):
    comentarios = Comentario.objects.all()
    return render(request, 'comentarios/ver_comentarios.html', {'comentarios': comentarios})

def actualizar_comentario(request, id_comentario):
    comentario = get_object_or_404(Comentario, pk=id_comentario)
    choferes = Chofer.objects.all()
    viajes = Viaje.objects.all()
    return render(request, 'comentarios/actualizar_comentario.html', {
        'comentario': comentario, 
        'choferes': choferes, 
        'viajes': viajes
    })

def realizar_actualizacion_comentario(request, id_comentario):
    if request.method == 'POST':
        comentario = get_object_or_404(Comentario, pk=id_comentario)
        comentario.chofer = get_object_or_404(Chofer, pk=request.POST['chofer'])
        comentario.viaje = get_object_or_404(Viaje, pk=request.POST['viaje'])
        comentario.comentario = request.POST['comentario']
        comentario.num_resena = request.POST.get('num_resena')
        comentario.save()
        return redirect('ver_comentarios')
    return redirect('ver_comentarios')

def borrar_comentario(request, id_comentario):
    comentario = get_object_or_404(Comentario, pk=id_comentario)
    if request.method == 'POST':
        comentario.delete()
        return redirect('ver_comentarios')
    return render(request, 'comentarios/borrar_comentario.html', {'comentario': comentario})


# ========================================================
# 7. PAGOS (CRUD simple)
# ========================================================

def agregar_pago(request):
    if request.method == 'POST':
        monto = request.POST['monto']
        metodo_pago = request.POST['metodo_pago']
        Pagos.objects.create(
            monto=monto,
            metodo_pago=metodo_pago
        )
        return redirect('ver_pagos')
    return render(request, 'pagos/agregar_pago.html')

def ver_pagos(request):
    pagos = Pagos.objects.all()
    return render(request, 'pagos/ver_pagos.html', {'pagos': pagos})

def actualizar_pago(request, id_pago):
    pago = get_object_or_404(Pagos, pk=id_pago)
    return render(request, 'pagos/actualizar_pago.html', {'pago': pago})

def realizar_actualizacion_pago(request, id_pago):
    if request.method == 'POST':
        pago = get_object_or_404(Pagos, pk=id_pago)
        pago.monto = request.POST['monto']
        pago.metodo_pago = request.POST['metodo_pago']
        pago.save()
        return redirect('ver_pagos')
    return redirect('ver_pagos')

def borrar_pago(request, id_pago):
    pago = get_object_or_404(Pagos, pk=id_pago)
    if request.method == 'POST':
        pago.delete()
        return redirect('ver_pagos')
    return render(request, 'pagos/borrar_pago.html', {'pago': pago})


# ========================================================
# 8. CUENTA DUEÑO (CRUD simple)
# ========================================================

def agregar_cuenta_dueno(request):
    if request.method == 'POST':
        nombre = request.POST['nombre'] # Aquí recibirá el nombre seleccionado
        por_chofer = request.POST['por_chofer']
        por_dueno = request.POST['por_dueno']

        CuentaDueno.objects.create(
            nombre=nombre,
            por_chofer=por_chofer,
            por_dueno=por_dueno
        )
        return redirect('ver_cuentas_dueno')
    
    # AGREGAMOS ESTO: Obtener los choferes para mandarlos al HTML
    choferes = Chofer.objects.all()
    return render(request, 'cuenta_dueno/agregar_cuenta_dueno.html', {'choferes': choferes})

def ver_cuentas_dueno(request):
    cuentas = CuentaDueno.objects.all()
    return render(request, 'cuenta_dueno/ver_cuentas_dueno.html', {'cuentas': cuentas})

def actualizar_cuenta_dueno(request, id_dueno):
    cuenta = get_object_or_404(CuentaDueno, pk=id_dueno)
    # AGREGAMOS ESTO: También necesitamos los choferes aquí por si quiere cambiarlo
    choferes = Chofer.objects.all()
    return render(request, 'cuenta_dueno/actualizar_cuenta_dueno.html', {'cuenta': cuenta, 'choferes': choferes})

def realizar_actualizacion_cuenta_dueno(request, id_dueno):
    if request.method == 'POST':
        cuenta = get_object_or_404(CuentaDueno, pk=id_dueno)
        cuenta.nombre = request.POST['nombre']
        cuenta.por_chofer = request.POST['por_chofer']
        cuenta.por_dueno = request.POST['por_dueno']
        cuenta.save()
        return redirect('ver_cuentas_dueno')
    return redirect('ver_cuentas_dueno')

def borrar_cuenta_dueno(request, id_dueno):
    cuenta = get_object_or_404(CuentaDueno, pk=id_dueno)
    if request.method == 'POST':
        cuenta.delete()
        return redirect('ver_cuentas_dueno')
    return render(request, 'cuenta_dueno/borrar_cuenta_dueno.html', {'cuenta': cuenta})