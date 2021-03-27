from django.db import models
from django.utils import timezone
from rest_framework import serializers


class Complemento(models.Model):
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion


class ComplementoDestino(models.Model):
    precio = models.FloatField(blank=True)
    estado = models.BooleanField(default=True)
    complemento = models.ForeignKey("Complemento", on_delete=models.DO_NOTHING)
    destino_turistico = models.ForeignKey("DestinoTuristico", on_delete=models.DO_NOTHING)


class DestinoTuristico(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.ForeignKey("Ciudad", on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
    departamento = models.ForeignKey('Departamento', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
    pais = models.ForeignKey('Pais', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre


class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre


# class ClientePlan(models.Model):
#     plan = models.ForeignKey('Plan', on_delete=models.DO_NOTHING)
#     cliente = models.ForeignKey('Cliente', on_delete=models.DO_NOTHING)
#     complementos = models.ManyToManyField(ComplementoDestino)


class Plan(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.CharField(max_length=455)
    fecha_ida = models.DateTimeField(null=True)
    fecha_regreso = models.DateTimeField(null=True)
    rating = models.IntegerField(null=True)
    precio = models.FloatField(null=True)
    destinos = models.ManyToManyField(DestinoTuristico, through='DestinoHotel', through_fields=('plan', 'destino'))

    def __str__(self):
        return self.titulo


class DestinoHotel(models.Model):
    plan = models.ForeignKey("Plan", on_delete=models.DO_NOTHING)
    destino = models.ForeignKey("DestinoTuristico", on_delete=models.DO_NOTHING)
    hotel = models.ForeignKey("Hotel", on_delete=models.DO_NOTHING, null=True)
    hotel_tipo_habitacion = models.ForeignKey("HotelTipoHabitacion", on_delete=models.DO_NOTHING, null=True)


class HotelTipoHabitacion(models.Model):
    precio = models.FloatField()
    capacidad = models.IntegerField()
    tipo_habitacion = models.ForeignKey("TipoHabitacion", on_delete=models.DO_NOTHING)
    hotel = models.ForeignKey("Hotel", on_delete=models.DO_NOTHING)


class TipoHabitacion(models.Model):
    descripcion = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion


class Servicio(models.Model):
    descripcion = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion


class Hotel(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(default=True)
    created = serializers.HiddenField(default=timezone.now())
    imagen = models.CharField(max_length=455)
    url = models.CharField(max_length=255)
    ciudad = models.ForeignKey("Ciudad", on_delete=models.DO_NOTHING)
    categoria = models.ForeignKey("Categoria", on_delete=models.DO_NOTHING, null=True)
    servicios = models.ManyToManyField(Servicio, through="HotelServicio", through_fields=('hotel', 'servicio'))
    tipo_habitaciones = models.ManyToManyField(TipoHabitacion, through="HotelTipoHabitacion",
                                               through_fields=('hotel', 'tipo_habitacion'))

    def __str__(self):
        return self.nombre


class HotelServicio(models.Model):
    precio = models.FloatField()
    servicio = models.ForeignKey("Servicio", on_delete=models.DO_NOTHING)
    hotel = models.ForeignKey("Hotel", on_delete=models.DO_NOTHING)


class Categoria(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion


class Cliente(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15, null=True)
    created = serializers.HiddenField(default=timezone.now())
    estado = models.BooleanField(default=True)
    referido = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True)
    uid = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "{} {}".format(self.nombres, self.apellidos)


class Promocion(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.CharField(max_length=455)
    plan = models.ForeignKey("Plan", on_delete=models.DO_NOTHING)


class Compras(models.Model):
    plan = models.ForeignKey("Plan", on_delete=models.DO_NOTHING)
    cliente = models.ForeignKey("Cliente", on_delete=models.DO_NOTHING)
    ciudad = models.ForeignKey("Ciudad", on_delete=models.DO_NOTHING)
    fecha_ida = models.DateField()
    fecha_regreso = models.DateField()
    precio = models.FloatField(null=True)
    hotel = models.ForeignKey("Hotel", on_delete=models.DO_NOTHING, null=True)
    servicios = models.ManyToManyField(Servicio, null=True)
    tipo_habitacion = models.ForeignKey("TipoHabitacion", on_delete=models.DO_NOTHING, null=True)
