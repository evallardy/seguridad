from django.urls import path

from .views import (
    DetalleMantenimientoCreateView,
    DetalleMantenimientoDeleteView,
    DetalleMantenimientoListView,
    DetalleMantenimientoUpdateView,
    HomeView,
    InspeccionCreateView,
    InspeccionDeleteView,
    InspeccionListView,
    InspeccionUpdateView,
    OrdenMantenimientoCreateView,
    OrdenMantenimientoDeleteView,
    OrdenMantenimientoListView,
    OrdenMantenimientoUpdateView,
    ProgramacionMantenimientoCreateView,
    ProgramacionMantenimientoDeleteView,
    ProgramacionMantenimientoListView,
    ProgramacionMantenimientoUpdateView,
)

app_name = "mantenimiento"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("ordenes/", OrdenMantenimientoListView.as_view(), name="orden_list"),
    path("ordenes/nuevo/", OrdenMantenimientoCreateView.as_view(), name="orden_create"),
    path(
        "ordenes/<int:pk>/editar/",
        OrdenMantenimientoUpdateView.as_view(),
        name="orden_update",
    ),
    path(
        "ordenes/<int:pk>/eliminar/",
        OrdenMantenimientoDeleteView.as_view(),
        name="orden_delete",
    ),
    path("detalles/", DetalleMantenimientoListView.as_view(), name="detalle_list"),
    path("detalles/nuevo/", DetalleMantenimientoCreateView.as_view(), name="detalle_create"),
    path(
        "detalles/<int:pk>/editar/",
        DetalleMantenimientoUpdateView.as_view(),
        name="detalle_update",
    ),
    path(
        "detalles/<int:pk>/eliminar/",
        DetalleMantenimientoDeleteView.as_view(),
        name="detalle_delete",
    ),
    path(
        "programaciones/",
        ProgramacionMantenimientoListView.as_view(),
        name="programacion_list",
    ),
    path(
        "programaciones/nuevo/",
        ProgramacionMantenimientoCreateView.as_view(),
        name="programacion_create",
    ),
    path(
        "programaciones/<int:pk>/editar/",
        ProgramacionMantenimientoUpdateView.as_view(),
        name="programacion_update",
    ),
    path(
        "programaciones/<int:pk>/eliminar/",
        ProgramacionMantenimientoDeleteView.as_view(),
        name="programacion_delete",
    ),
    path("inspecciones/", InspeccionListView.as_view(), name="inspeccion_list"),
    path("inspecciones/nuevo/", InspeccionCreateView.as_view(), name="inspeccion_create"),
    path(
        "inspecciones/<int:pk>/editar/",
        InspeccionUpdateView.as_view(),
        name="inspeccion_update",
    ),
    path(
        "inspecciones/<int:pk>/eliminar/",
        InspeccionDeleteView.as_view(),
        name="inspeccion_delete",
    ),
]
