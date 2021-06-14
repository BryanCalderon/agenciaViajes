from statistics import mean

from django.contrib.auth.models import Group, User
from django.utils.timezone import now

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


class FechaPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FechaPlan
        fields = '__all__'

    def get_plans_by_future_dates(self):
        return FechaPlan.objects.filter(fecha_ida__gte=now()).distinct("plan").prefetch_related("plan")

    def get_by_plan(self, plan_id):
        return FechaPlan.objects.filter(plan=plan_id, fecha_ida__gte=now()).values()


class PlanSerializer(serializers.HyperlinkedModelSerializer):
    fechas = FechaPlanSerializer(many=True, read_only=True)
    precioMinimo = serializers.SerializerMethodField(method_name='get_min_price')
    rating = serializers.SerializerMethodField()
    totalRating = serializers.SerializerMethodField()
    totalDias = serializers.SerializerMethodField(method_name='get_days')

    class Meta:
        model = Plan
        fields = ['id', 'titulo', 'descripcion', 'imagen', 'fechas', 'precioMinimo', 'rating', 'totalDias',
                  'totalRating']

    def get_min_price(self, obj):
        min_item = self.get_min_fecha_plan_by_price(obj)
        if min_item:
            return min_item.precio
        return None

    def get_min_fecha_plan_by_price(self, obj):
        fechas = FechaPlan.objects.filter(plan=obj, fecha_ida__gte=now())
        min_item = None

        for item in fechas:
            if min_item is None:
                min_item = item
                continue

            if min_item.precio < item.precio:
                min_item = min_item
            else:
                min_item = item

        return min_item

    def get_rating(self, obj):
        reviews = Review.objects.filter(plan=obj)
        if not reviews:
            return None
        return round(mean(map(lambda item: item.calificacion, reviews)), 2)

    def get_totalRating(self, obj):
        return Review.objects.filter(plan=obj).count()

    def get_days(self, obj):
        min_item = self.get_min_fecha_plan_by_price(obj)
        if min_item:
            d1 = min_item.fecha_ida
            d2 = min_item.fecha_regreso
            diff = abs((d2 - d1).days)
            return diff
        else:
            return None


class HabitacionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Habitacion
        fields = ['id', 'descripcion']


class HotelHabitacionSerializer(serializers.HyperlinkedModelSerializer):
    habitacion = HabitacionSerializer(read_only=True)

    class Meta:
        model = HotelHabitacion
        fields = '__all__'


class HotelSerializer(serializers.HyperlinkedModelSerializer):
    hotel_habitaciones = HotelHabitacionSerializer(many=True, read_only=True)
    ciudad = CiudadSerializer

    class Meta:
        model = Hotel
        fields = ['id', 'nombre', 'descripcion', 'url', 'estado', 'imagen', 'hotel_habitaciones', 'ciudad']


class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombres', 'apellidos', 'identificacion', 'email', 'fecha_nacimiento', 'telefono', 'uid']


class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
