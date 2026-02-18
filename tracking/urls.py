from django.urls import path

from .views import (
    DispositivoCreateView,
    DispositivoDeleteView,
    DispositivoListView,
    DispositivoUpdateView,
    HomeView,
    PermisoGPSCreateView,
    PermisoGPSDeleteView,
    PermisoGPSListView,
    PermisoGPSUpdateView,
    UbicacionCreateView,
    UbicacionDeleteView,
    UbicacionListView,
    UbicacionUpdateView,
)

app_name = "tracking"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("dispositivos/", DispositivoListView.as_view(), name="dispositivo_list"),
    path("dispositivos/nuevo/", DispositivoCreateView.as_view(), name="dispositivo_create"),
    path(
        "dispositivos/<int:pk>/editar/",
        DispositivoUpdateView.as_view(),
        name="dispositivo_update",
    ),
    path(
        "dispositivos/<int:pk>/eliminar/",
        DispositivoDeleteView.as_view(),
        name="dispositivo_delete",
    ),
    path("permisos/", PermisoGPSListView.as_view(), name="permiso_list"),
    path("permisos/nuevo/", PermisoGPSCreateView.as_view(), name="permiso_create"),
    path(
        "permisos/<int:pk>/editar/",
        PermisoGPSUpdateView.as_view(),
        name="permiso_update",
    ),
    path(
        "permisos/<int:pk>/eliminar/",
        PermisoGPSDeleteView.as_view(),
        name="permiso_delete",
    ),
    path("ubicaciones/", UbicacionListView.as_view(), name="ubicacion_list"),
    path("ubicaciones/nuevo/", UbicacionCreateView.as_view(), name="ubicacion_create"),
    path(
        "ubicaciones/<int:pk>/editar/",
        UbicacionUpdateView.as_view(),
        name="ubicacion_update",
    ),
    path(
        "ubicaciones/<int:pk>/eliminar/",
        UbicacionDeleteView.as_view(),
        name="ubicacion_delete",
    ),
]
