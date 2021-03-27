from django.contrib.auth.models import Group, User
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PaisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pais
        fields = ['id', 'nombre']


class DepartamentoSerializer(serializers.HyperlinkedModelSerializer):
    pais = PaisSerializer(read_only=True)

    class Meta:
        model = Departamento
        fields = ['id', 'nombre', 'pais']


class CiudadSerializer(serializers.HyperlinkedModelSerializer):
    departamento = DepartamentoSerializer()

    class Meta:
        model = Ciudad
        fields = ['id', 'url', 'nombre', 'departamento']


class DestinoTuristicoSerializer(serializers.HyperlinkedModelSerializer):
    ciudad = CiudadSerializer()

    class Meta:
        model = DestinoTuristico
        fields = ['id', 'nombre', 'estado', 'ciudad']


class PlanSerializer(serializers.HyperlinkedModelSerializer):
    destinos = DestinoTuristicoSerializer(many=True, read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'titulo', 'descripcion', 'imagen', 'fecha_ida', 'fecha_regreso', 'rating', 'precio', 'destinos']


class ServicioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'descripcion', 'estado']


class TipoHabitacionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TipoHabitacion
        fields = ['id', 'descripcion']


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'descripcion']


class HotelSerializer(serializers.HyperlinkedModelSerializer):
    servicios = ServicioSerializer(many=True, read_only=True)
    tipo_habitaciones = TipoHabitacionSerializer(many=True, read_only=True)
    ciudad = CiudadSerializer
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'url', 'nombre', 'descripcion', 'estado', 'imagen', 'servicios', 'tipo_habitaciones', 'ciudad',
                  'categoria']


class HotelServicioSerializer(serializers.HyperlinkedModelSerializer):
    # hotel = HotelSerializer(read_only=True)
    servicio = ServicioSerializer(read_only=True)

    class Meta:
        model = HotelServicio
        fields = '__all__'


class HotelTipoHabitacionSerializer(serializers.HyperlinkedModelSerializer):
    # hotel = HotelSerializer(read_only=True)
    tipo_habitacion = TipoHabitacionSerializer(read_only=True)

    class Meta:
        model = HotelTipoHabitacion
        fields = '__all__'


class DestinoHotelSerializer(serializers.HyperlinkedModelSerializer):
    plan = PlanSerializer(read_only=True)
    destino = DestinoTuristicoSerializer(read_only=True)
    hotel = HotelSerializer(read_only=True)
    hotel_tipo_habitacion = HotelTipoHabitacionSerializer(read_only=True)

    class Meta:
        model = DestinoHotel
        fields = '__all__'


class ComplementoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Complemento
        fields = ['id', 'descripcion', 'estado']


class ComplementoDestinoSerializer(serializers.HyperlinkedModelSerializer):
    complemento = ComplementoSerializer(read_only=True)
    destino_turistico = DestinoTuristicoSerializer(read_only=True)

    class Meta:
        model = ComplementoDestino
        fields = '__all__'


class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        # fields = '__all__'
        fields = ['id', 'nombres', 'apellidos', 'identificacion', 'email', 'fecha_nacimiento', 'telefono', 'uid']


# class ClientePlanSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ClientePlan
#         fields = '__all__'


class PromocionSerializer(serializers.HyperlinkedModelSerializer):
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = Promocion
        fields = '__all__'


class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compras
        fields = '__all__'
