"""backend_agencia_viajes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'complementos', views.ComplementoViewSet)
router.register(r'complementos-destino', views.ComplementoDestinoViewSet)
router.register(r'destinos', views.DestinoTuristicoViewSet)
router.register(r'ciudades', views.CiudadViewSet)
router.register(r'departamentos', views.DepartamentoViewSet)
router.register(r'paises', views.PaisViewSet)
# router.register(r'clientes-plan', views.ClientePlanViewSet)
router.register(r'planes', views.PlanViewSet)
router.register(r'destino-hotel', views.DestinoHotelViewSet)
router.register(r'hotel', views.HotelViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'clientes', views.ClienteViewSet)
router.register(r'promocion', views.PromocionViewSet)
router.register(r'hotel-tipo-habitacion', views.HotelTipoHabitacionViewSet)
router.register(r'tipo-habitacion', views.TipoHabitacionViewSet)
router.register(r'hotel-servicio', views.HotelServicioViewSet)
router.register(r'servicios', views.ServicioViewSet)
router.register(r'compra', views.CompraViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
