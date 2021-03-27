from http import HTTPStatus

from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class DestinoTuristicoViewSet(viewsets.ModelViewSet):
    queryset = DestinoTuristico.objects.all()
    serializer_class = DestinoTuristicoSerializer


class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

    @action(detail=True, methods=['get'], url_path='cities')
    def getCitiesByDepartment(self, request, pk=None):
        cities = Ciudad.objects.filter(departamento=pk)
        serializer = CiudadSerializer(cities, many=True, context={'request': request})
        return Response(serializer.data)


class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer


class ComplementoViewSet(viewsets.ModelViewSet):
    queryset = Complemento.objects.all()
    serializer_class = ComplementoSerializer


class ComplementoDestinoViewSet(viewsets.ModelViewSet):
    queryset = ComplementoDestino.objects.all()
    serializer_class = ComplementoDestinoSerializer


class DestinoHotelViewSet(viewsets.ModelViewSet):
    queryset = DestinoHotel.objects.all()
    serializer_class = DestinoHotelSerializer


#
# class ClientePlanViewSet(viewsets.ModelViewSet):
#     queryset = ClientePlan.objects.all()
#     serializer_class = ClientePlanSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @action(detail=False, methods=['get'], url_path='byUid/(?P<uid_pk>[^/.]+)')
    def by_uid(self, request, uid_pk):
        client = Cliente.objects.filter(uid=uid_pk).first()
        if client:
            serializer = ClienteSerializer(client, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'message': 'Client with UID {} not found'.format(uid_pk)},
                            status=status.HTTP_404_NOT_FOUND)


class PromocionViewSet(viewsets.ModelViewSet):
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer


class HotelTipoHabitacionViewSet(viewsets.ModelViewSet):
    queryset = HotelTipoHabitacion.objects.all()
    serializer_class = HotelTipoHabitacionSerializer

    @action(detail=False, methods=['get'], url_path='getByHotel/(?P<hotel_pk>[^/.]+)')
    def getByHotel(self, request, hotel_pk=None):
        hth = HotelTipoHabitacion.objects.filter(hotel=hotel_pk)
        serializer = HotelTipoHabitacionSerializer(hth, many=True, context={'request': request})
        return Response(serializer.data)


class TipoHabitacionViewSet(viewsets.ModelViewSet):
    queryset = TipoHabitacion.objects.all()
    serializer_class = TipoHabitacionSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    @action(detail=False, methods=['get'], url_path='byCity/(?P<city_pk>[^/.]+)')
    def hotelsByCity(self, request, city_pk=None):
        hotels = Hotel.objects.filter(ciudad=city_pk)
        serializer = HotelSerializer(hotels, many=True, context={'request': request})
        return Response(serializer.data)


class HotelServicioViewSet(viewsets.ModelViewSet):
    queryset = HotelServicio.objects.all()
    serializer_class = HotelServicioSerializer

    @action(detail=False, methods=['get'], url_path='getByHotel/(?P<hotel_pk>[^/.]+)')
    def getByHotel(self, request, hotel_pk=None):
        hs = HotelServicio.objects.filter(hotel=hotel_pk)
        serializer = HotelServicioSerializer(hs, many=True, context={'request': request})
        return Response(serializer.data)


class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compras.objects.all()
    serializer_class = CompraSerializer

    def create(self, request, *args, **kwargs):
        referidos = request.data['referidos']
        main_client = Cliente.objects.filter(id=request.data['cliente']['id']).first()
        if main_client:
            for re in referidos:
                pasajero = ClienteSerializer(data=re)
                if pasajero.is_valid():
                    referido: Cliente = Cliente.objects \
                        .filter(identificacion=pasajero.validated_data['identificacion']) \
                        .first()
                    if referido:
                        referido.nombres = pasajero.validated_data['nombres']
                        referido.apellidos = pasajero.validated_data['apellidos']
                        referido.email = pasajero.validated_data['email']
                        referido.telefono = pasajero.validated_data.get('telefono')
                        referido.fecha_nacimiento = pasajero.validated_data['fecha_nacimiento']

                        if referido.referido is None:
                            referido.referido = main_client
                        referido.save()
                    else:
                        cliente = Cliente(**pasajero.validated_data)
                        cliente.referido = main_client
                        cliente.save()

            plan = Plan.objects.filter(id=request.data['plan']['id']).first()
            ciudad = Ciudad.objects.filter(id=request.data['ciudad']['id']).first()

            hotel = None
            if request.data['hotel']:
                hotel = Hotel.objects.filter(id=request.data['hotel']['id']).first()

            tipo_habitacion = None
            if request.data['tipo_habitacion']:
                tipo_habitacion = TipoHabitacion.objects.filter(
                    id=request.data['tipo_habitacion']['tipo_habitacion']['id']).first()

            compra = Compras(
                plan=plan,
                cliente=main_client,
                ciudad=ciudad,
                fecha_ida=request.data.get("fecha_ida"),
                fecha_regreso=request.data.get("fecha_regreso"),
                precio=request.data.get("precio"),
                hotel=hotel,
                tipo_habitacion=tipo_habitacion
            )
            compra.save()
            return Response(status=HTTPStatus.CREATED)
