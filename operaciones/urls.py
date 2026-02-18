from django.urls import path

from .views import (
    ClienteCreateView,
    ClienteDeleteView,
    ClienteListView,
    ClienteUpdateView,
    ContratoCreateView,
    ContratoDeleteView,
    ContratoListView,
    ContratoUpdateView,
    HomeView,
    ServicioCreateView,
    ServicioDeleteView,
    ServicioListView,
    ServicioUpdateView,
    SitioCreateView,
    SitioDeleteView,
    SitioListView,
    SitioUpdateView,
)

app_name = "operaciones"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("clientes/", ClienteListView.as_view(), name="cliente_list"),
    path("clientes/nuevo/", ClienteCreateView.as_view(), name="cliente_create"),
    path("clientes/<int:pk>/editar/", ClienteUpdateView.as_view(), name="cliente_update"),
    path("clientes/<int:pk>/eliminar/", ClienteDeleteView.as_view(), name="cliente_delete"),
    path("sitios/", SitioListView.as_view(), name="sitio_list"),
    path("sitios/nuevo/", SitioCreateView.as_view(), name="sitio_create"),
    path("sitios/<int:pk>/editar/", SitioUpdateView.as_view(), name="sitio_update"),
    path("sitios/<int:pk>/eliminar/", SitioDeleteView.as_view(), name="sitio_delete"),
    path("servicios/", ServicioListView.as_view(), name="servicio_list"),
    path("servicios/nuevo/", ServicioCreateView.as_view(), name="servicio_create"),
    path("servicios/<int:pk>/editar/", ServicioUpdateView.as_view(), name="servicio_update"),
    path("servicios/<int:pk>/eliminar/", ServicioDeleteView.as_view(), name="servicio_delete"),
    path("contratos/", ContratoListView.as_view(), name="contrato_list"),
    path("contratos/nuevo/", ContratoCreateView.as_view(), name="contrato_create"),
    path("contratos/<int:pk>/editar/", ContratoUpdateView.as_view(), name="contrato_update"),
    path("contratos/<int:pk>/eliminar/", ContratoDeleteView.as_view(), name="contrato_delete"),
]
