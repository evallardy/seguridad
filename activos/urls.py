from django.urls import path

from .views import (
    ArmamentoCreateView,
    ArmamentoDeleteView,
    ArmamentoListView,
    ArmamentoUpdateView,
    AsignacionActivoCreateView,
    AsignacionActivoDeleteView,
    AsignacionActivoListView,
    AsignacionActivoUpdateView,
    HomeView,
    RegistroCombustibleCreateView,
    RegistroCombustibleDeleteView,
    RegistroCombustibleListView,
    RegistroCombustibleUpdateView,
    RefaccionCreateView,
    RefaccionDeleteView,
    RefaccionListView,
    RefaccionUpdateView,
    VehiculoCreateView,
    VehiculoDeleteView,
    VehiculoListView,
    VehiculoUpdateView,
)

app_name = "activos"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("vehiculos/", VehiculoListView.as_view(), name="vehiculo_list"),
    path("vehiculos/nuevo/", VehiculoCreateView.as_view(), name="vehiculo_create"),
    path("vehiculos/<int:pk>/editar/", VehiculoUpdateView.as_view(), name="vehiculo_update"),
    path("vehiculos/<int:pk>/eliminar/", VehiculoDeleteView.as_view(), name="vehiculo_delete"),
    path("armamento/", ArmamentoListView.as_view(), name="armamento_list"),
    path("armamento/nuevo/", ArmamentoCreateView.as_view(), name="armamento_create"),
    path("armamento/<int:pk>/editar/", ArmamentoUpdateView.as_view(), name="armamento_update"),
    path("armamento/<int:pk>/eliminar/", ArmamentoDeleteView.as_view(), name="armamento_delete"),
    path("refacciones/", RefaccionListView.as_view(), name="refaccion_list"),
    path("refacciones/nuevo/", RefaccionCreateView.as_view(), name="refaccion_create"),
    path("refacciones/<int:pk>/editar/", RefaccionUpdateView.as_view(), name="refaccion_update"),
    path("refacciones/<int:pk>/eliminar/", RefaccionDeleteView.as_view(), name="refaccion_delete"),
    path("asignaciones/", AsignacionActivoListView.as_view(), name="asignacion_activo_list"),
    path(
        "asignaciones/nuevo/",
        AsignacionActivoCreateView.as_view(),
        name="asignacion_activo_create",
    ),
    path(
        "asignaciones/<int:pk>/editar/",
        AsignacionActivoUpdateView.as_view(),
        name="asignacion_activo_update",
    ),
    path(
        "asignaciones/<int:pk>/eliminar/",
        AsignacionActivoDeleteView.as_view(),
        name="asignacion_activo_delete",
    ),
    path(
        "combustible/",
        RegistroCombustibleListView.as_view(),
        name="registro_combustible_list",
    ),
    path(
        "combustible/nuevo/",
        RegistroCombustibleCreateView.as_view(),
        name="registro_combustible_create",
    ),
    path(
        "combustible/<int:pk>/editar/",
        RegistroCombustibleUpdateView.as_view(),
        name="registro_combustible_update",
    ),
    path(
        "combustible/<int:pk>/eliminar/",
        RegistroCombustibleDeleteView.as_view(),
        name="registro_combustible_delete",
    ),
]
