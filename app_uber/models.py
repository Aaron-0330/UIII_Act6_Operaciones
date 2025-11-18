# app_uber/models.py
# app_uber/models.py
from django.db import models

# ==========================================
# MODELO: Chofer (Tu código)
# ==========================================
class Chofer(models.Model):
    id_chofer = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    licencia = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    edad = models.IntegerField()
    fecha_ingreso = models.DateField()

    def __str__(self):
        return self.nombre


# ==========================================
# MODELO: Usuario_pasajero (Tu código)
# ==========================================
class UsuarioPasajero(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=150)
    fecha_registro = models.DateField()
    genero = models.CharField(max_length=10)
    ciudad = models.CharField(max_length=100)
    # Relación 1:N con Chofer (un chofer puede ser preferido por muchos pasajeros)
    chofer_preferido = models.ForeignKey(Chofer, on_delete=models.SET_NULL, null=True, blank=True, related_name='pasajeros_preferidos')

    def __str__(self):
        return self.nombre


# ==========================================
# MODELO: Pagos (Nuevo - Necesario para Viaje)
# ==========================================
class Pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50) # Ej: Efectivo, Tarjeta
    fecha_pago = models.DateTimeField(auto_now_add=True) # Se guarda automático al crear

    def __str__(self):
        return f"Pago ${self.monto} ({self.metodo_pago})"


# ==========================================
# MODELO: Viaje (Tu código + Relación Pago)
# ==========================================
class Viaje(models.Model):
    id_viaje = models.AutoField(primary_key=True)
    destino = models.CharField(max_length=100)
    fecha = models.DateField()
    hora_salida = models.TimeField()
    duracion = models.CharField(max_length=50) 
    costo = models.DecimalField(max_digits=8, decimal_places=2)
    estatus = models.CharField(max_length=20)

    # 🔹 Relación 1:N con Chofer
    chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE, related_name='viajes')

    # 🔹 Relación N:M con UsuarioPasajero
    pasajeros = models.ManyToManyField(UsuarioPasajero, related_name='viajes')

    # 🔹 NUEVO: Relación con Pagos (Para cumplir con el diagrama y vistas)
    pago = models.ForeignKey(Pagos, on_delete=models.SET_NULL, null=True, blank=True, related_name='viajes')
    
    # Nota: Agregué 'calificacion' aquí porque en el views anterior lo usábamos, 
    # si no lo quieres, bórralo, pero el diagrama original lo tenía.
    calificacion = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True) 

    def __str__(self):
        return f"Viaje a {self.destino} con {self.chofer.nombre}"


# ==========================================
# MODELO: Vehiculo (Nuevo)
# ==========================================
class Vehiculo(models.Model):
    # Relación con Chofer (Asumimos que un chofer tiene un vehículo asignado)
    chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE, related_name='vehiculos')
    marca_carro = models.CharField(max_length=50)
    modelo_carro = models.CharField(max_length=50)
    matricula = models.CharField(max_length=20, unique=True)
    tipo_carro = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.marca_carro} - {self.matricula}"


# ==========================================
# MODELO: Tarjetas (Nuevo)
# ==========================================
class Tarjetas(models.Model):
    usuario = models.ForeignKey(UsuarioPasajero, on_delete=models.CASCADE, related_name='tarjetas')
    numero_tarjeta = models.CharField(max_length=20)
    tipo_tarjeta = models.CharField(max_length=50)
    fecha_vencimiento = models.DateField()
    cv = models.IntegerField()

    def __str__(self):
        return f"Tarjeta {self.tipo_tarjeta} - {self.numero_tarjeta[-4:]}"


# ==========================================
# MODELO: Comentario (Nuevo)
# ==========================================
class Comentario(models.Model):
    chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE, related_name='comentarios')
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='comentarios')
    comentario = models.TextField()
    num_resena = models.IntegerField(default=0)
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario para {self.chofer.nombre}"


# ==========================================
# MODELO: CuentaDueño (Nuevo)
# ==========================================
class CuentaDueno(models.Model):
    id_dueno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    por_chofer = models.IntegerField(help_text="Porcentaje ganancia chofer")
    por_dueno = models.IntegerField(help_text="Porcentaje ganancia dueño")

    def __str__(self):
        return self.nombre