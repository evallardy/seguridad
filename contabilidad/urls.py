from django.urls import path

from .views import (
    CentroCostoCreateView,
    CentroCostoDeleteView,
    CentroCostoListView,
    CentroCostoUpdateView,
    CuentaCreateView,
    CuentaDeleteView,
    CuentaListView,
    CuentaUpdateView,
    FacturaCreateView,
    FacturaDeleteView,
    FacturaListView,
    FacturaUpdateView,
    HomeView,
    MovimientoCreateView,
    MovimientoDeleteView,
    MovimientoListView,
    MovimientoUpdateView,
    RelacionCentroCostoCreateView,
    RelacionCentroCostoDeleteView,
    RelacionCentroCostoListView,
    RelacionCentroCostoUpdateView,
)

app_name = "contabilidad"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("cuentas/", CuentaListView.as_view(), name="cuenta_list"),
    path("cuentas/nuevo/", CuentaCreateView.as_view(), name="cuenta_create"),
    path("cuentas/<int:pk>/editar/", CuentaUpdateView.as_view(), name="cuenta_update"),
    path("cuentas/<int:pk>/eliminar/", CuentaDeleteView.as_view(), name="cuenta_delete"),
    path("centros-costo/", CentroCostoListView.as_view(), name="centro_costo_list"),
    path(
        "centros-costo/nuevo/",
        CentroCostoCreateView.as_view(),
        name="centro_costo_create",
    ),
    path(
        "centros-costo/<int:pk>/editar/",
        CentroCostoUpdateView.as_view(),
        name="centro_costo_update",
    ),
    path(
        "centros-costo/<int:pk>/eliminar/",
        CentroCostoDeleteView.as_view(),
        name="centro_costo_delete",
    ),
    path("movimientos/", MovimientoListView.as_view(), name="movimiento_list"),
    path("movimientos/nuevo/", MovimientoCreateView.as_view(), name="movimiento_create"),
    path(
        "movimientos/<int:pk>/editar/",
        MovimientoUpdateView.as_view(),
        name="movimiento_update",
    ),
    path(
        "movimientos/<int:pk>/eliminar/",
        MovimientoDeleteView.as_view(),
        name="movimiento_delete",
    ),
    path(
        "relaciones-centro/",
        RelacionCentroCostoListView.as_view(),
        name="relacion_centro_costo_list",
    ),
    path(
        "relaciones-centro/nuevo/",
        RelacionCentroCostoCreateView.as_view(),
        name="relacion_centro_costo_create",
    ),
    path(
        "relaciones-centro/<int:pk>/editar/",
        RelacionCentroCostoUpdateView.as_view(),
        name="relacion_centro_costo_update",
    ),
    path(
        "relaciones-centro/<int:pk>/eliminar/",
        RelacionCentroCostoDeleteView.as_view(),
        name="relacion_centro_costo_delete",
    ),
    path("facturas/", FacturaListView.as_view(), name="factura_list"),
    path("facturas/nuevo/", FacturaCreateView.as_view(), name="factura_create"),
    path("facturas/<int:pk>/editar/", FacturaUpdateView.as_view(), name="factura_update"),
    path("facturas/<int:pk>/eliminar/", FacturaDeleteView.as_view(), name="factura_delete"),
]
