from django.db import models
from django.utils import timezone
from rest_framework import serializers


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


class Plan(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.CharField(max_length=455)

    def __str__(self):
        return self.titulo


class FechaPlan(models.Model):
    fecha_ida = models.DateTimeField(null=True)
    fecha_regreso = models.DateTimeField(null=True)
    precio = models.FloatField(null=True)
    plan = models.ForeignKey('Plan', related_name='fechas', on_delete=models.DO_NOTHING)


class Habitacion(models.Model):
    descripcion = models.CharField(max_length=100)

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

    def __str__(self):
        return self.nombre


class HotelHabitacion(models.Model):
    precio = models.FloatField()
    capacidad = models.IntegerField()
    habitacion = models.ForeignKey("Habitacion", on_delete=models.DO_NOTHING)
    hotel = models.ForeignKey("Hotel", on_delete=models.DO_NOTHING)


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


class Factura(models.Model):
    plan = models.ForeignKey("Plan", on_delete=models.DO_NOTHING)
    cliente = models.ForeignKey("Cliente", on_delete=models.DO_NOTHING)
    fechas = models.ForeignKey("FechaPlan", on_delete=models.DO_NOTHING)
    valor_pagar = models.FloatField()
    hotel = models.ForeignKey("Hotel", on_delete=models.DO_NOTHING, null=True)
    hotel_habitacion = models.ForeignKey("HotelHabitacion", on_delete=models.DO_NOTHING, null=True)


class Review(models.Model):
    comentario = models.CharField(max_length=455)
    created = models.DateTimeField(auto_created=True, auto_now=True, editable=False)
    calificacion = models.IntegerField(null=True)
    plan = models.ForeignKey("Plan", on_delete=models.DO_NOTHING)
    cliente = models.ForeignKey("Cliente", on_delete=models.DO_NOTHING)
