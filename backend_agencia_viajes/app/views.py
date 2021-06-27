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

    def list(self, request, *args, **kwargs):
        planes = PlanSerializer.get_plans_with_future_dates(self, None)
        page = self.paginate_queryset(planes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(planes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        plan_id = kwargs.get("pk")
        plan = Plan.objects.filter(id=plan_id).first()
        if plan:
            dates = FechaPlanSerializer.get_by_plan(self, plan_id)
            if dates and dates.count() > 0:
                serializer = PlanSerializer(plan, context={'request': request})
                return Response(serializer.data)

            return Response({'message': 'Plan with ID {} is not available'.format(plan_id)},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Plan with ID {} not found'.format(plan_id)},
                        status=status.HTTP_404_NOT_FOUND)


class FechaPlanViewSet(viewsets.ModelViewSet):
    queryset = FechaPlan.objects.all()
    serializer_class = FechaPlanSerializer


class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

    @action(detail=False, url_path='cities')
    def getCitiesByDepartment(self, request, pk=None):
        cities = Ciudad.objects.filter(departamento=pk)
        serializer = CiudadSerializer(cities, many=True, context={'request': request})
        return Response(serializer.data)


class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer


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


class HotelHabitacionViewSet(viewsets.ModelViewSet):
    queryset = HotelHabitacion.objects.all()
    serializer_class = HotelHabitacionSerializer

    @action(detail=False, methods=['get'], url_path='getByHotel/(?P<hotel_pk>[^/.]+)')
    def getByHotel(self, request, hotel_pk=None):
        hth = HotelHabitacion.objects.filter(hotel=hotel_pk)
        serializer = HotelHabitacionSerializer(hth, many=True, context={'request': request})
        return Response(serializer.data)


class HabitacionViewSet(viewsets.ModelViewSet):
    queryset = Habitacion.objects.all()
    serializer_class = HabitacionSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    @action(detail=False, methods=['get'], url_path='byCity/(?P<city_pk>[^/.]+)')
    def hotelsByCity(self, request, city_pk=None):
        hotels = Hotel.objects.filter(ciudad=city_pk)
        serializer = HotelSerializer(hotels, many=True, context={'request': request})
        return Response(serializer.data)


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

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

            hotel_habitacion = None
            if request.data['hotel_habitacion']:
                hotel_habitacion = HotelHabitacion.objects.filter(
                    id=request.data['hotel_habitacion']['hotel_habitacion']['id']).first()

            factura = Factura(
                plan=plan,
                cliente=main_client,
                ciudad=ciudad,
                # fecha_ida=request.data.get("fecha_ida"),
                # fecha_regreso=request.data.get("fecha_regreso"),
                precio=request.data.get("precio"),
                hotel=hotel,
                hotel_habitacion=hotel_habitacion
            )
            factura.save()
            return Response(status=HTTPStatus.CREATED)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @action(detail=False, methods=['get'], url_path='plan/(?P<plan_id>[^/.]+)')
    def get_reviews_by_plan(self, request, plan_id=None):
        reviews = Review.objects.filter(plan=plan_id)
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)
