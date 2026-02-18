from django.urls import path

from .views import (
    AsignacionCreateView,
    AsignacionDeleteView,
    AsignacionEmpleadoCreateView,
    AsignacionEmpleadoDeleteView,
    AsignacionEmpleadoListView,
    AsignacionEmpleadoUpdateView,
    AsignacionListView,
    AsignacionUpdateView,
    EquipoCreateView,
    EquipoDeleteView,
    EquipoListView,
    EquipoUpdateView,
    HomeView,
    RutaCreateView,
    RutaDeleteView,
    RutaListView,
    RutaPuntoCreateView,
    RutaPuntoDeleteView,
    RutaPuntoListView,
    RutaPuntoUpdateView,
    RutaUpdateView,
)

app_name = "asignaciones"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("rutas/", RutaListView.as_view(), name="ruta_list"),
    path("rutas/nuevo/", RutaCreateView.as_view(), name="ruta_create"),
    path("rutas/<int:pk>/editar/", RutaUpdateView.as_view(), name="ruta_update"),
    path("rutas/<int:pk>/eliminar/", RutaDeleteView.as_view(), name="ruta_delete"),
    path("rutas/<int:ruta_id>/puntos/", RutaPuntoListView.as_view(), name="ruta_punto_list"),
    path(
        "rutas/<int:ruta_id>/puntos/nuevo/",
        RutaPuntoCreateView.as_view(),
        name="ruta_punto_create",
    ),
    path(
        "rutas/<int:pk>/puntos/editar/",
        RutaPuntoUpdateView.as_view(),
        name="ruta_punto_update",
    ),
    path(
        "rutas/<int:pk>/puntos/eliminar/",
        RutaPuntoDeleteView.as_view(),
        name="ruta_punto_delete",
    ),
    path("equipos/", EquipoListView.as_view(), name="equipo_list"),
    path("equipos/nuevo/", EquipoCreateView.as_view(), name="equipo_create"),
    path("equipos/<int:pk>/editar/", EquipoUpdateView.as_view(), name="equipo_update"),
    path("equipos/<int:pk>/eliminar/", EquipoDeleteView.as_view(), name="equipo_delete"),
    path("asignaciones/", AsignacionListView.as_view(), name="asignacion_list"),
    path("asignaciones/nuevo/", AsignacionCreateView.as_view(), name="asignacion_create"),
    path("asignaciones/<int:pk>/editar/", AsignacionUpdateView.as_view(), name="asignacion_update"),
    path("asignaciones/<int:pk>/eliminar/", AsignacionDeleteView.as_view(), name="asignacion_delete"),
    path(
        "asignaciones-empleado/",
        AsignacionEmpleadoListView.as_view(),
        name="asignacion_empleado_list",
    ),
    path(
        "asignaciones-empleado/nuevo/",
        AsignacionEmpleadoCreateView.as_view(),
        name="asignacion_empleado_create",
    ),
    path(
        "asignaciones-empleado/<int:pk>/editar/",
        AsignacionEmpleadoUpdateView.as_view(),
        name="asignacion_empleado_update",
    ),
    path(
        "asignaciones-empleado/<int:pk>/eliminar/",
        AsignacionEmpleadoDeleteView.as_view(),
        name="asignacion_empleado_delete",
    ),
]
