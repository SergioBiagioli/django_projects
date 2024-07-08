from django.urls import path
from . import views
from .views import (
    EmpresaListView, 
    SucursalListView, 
    EgresoCiertoListView, 
    EgresoPresupuestadoListView, 
    PresupuestoMensualFijoListView, 
    IngresoCiertoListView, 
    IngresoPrevisionadoListView, 
    EmpresaCreateView, 
    EmpresaUpdateView, 
    EmpresaDeleteView, 
    SucursalCreateView, 
    SucursalUpdateView, 
    SucursalDeleteView, 
    EgresoCiertoCreateView, 
    EgresoCiertoUpdateView, 
    EgresoCiertoDeleteView, 
    EgresoPresupuestadoCreateView, 
    EgresoPresupuestadoUpdateView, 
    EgresoPresupuestadoDeleteView, 
    PresupuestoMensualFijoCreateView, 
    PresupuestoMensualFijoUpdateView, 
    PresupuestoMensualFijoDeleteView, 
    IngresoCiertoCreateView, 
    IngresoCiertoUpdateView, 
    IngresoCiertoDeleteView, 
    IngresoPrevisionadoCreateView, 
    IngresoPrevisionadoUpdateView, 
    IngresoPrevisionadoDeleteView
)


app_name = 'cashmanagement'
urlpatterns = [
    #path('', views.EmpresaListView.as_view(), name='all'),
    path('empresas/', views.EmpresaListView.as_view(), name='empresa_list'),
    path('empresas/new/', views.EmpresaCreateView.as_view, name='empresa_create'),
    path('empresas/edit/<int:pk>/', views.EmpresaUpdateView.as_view, name='empresa_update'),
    path('empresas/delete/<int:pk>/', views.EmpresaDeleteView.as_view, name='empresa_delete'),]

#     path('sucursales/', sucursal_list, name='sucursal_list'),
#     path('sucursales/new/', sucursal_create, name='sucursal_create'),
#     path('sucursales/edit/<int:pk>/', sucursal_update, name='sucursal_update'),
#     path('sucursales/delete/<int:pk>/', sucursal_delete, name='sucursal_delete'),

#     path('egreso_cierto/', egreso_cierto_list, name='egreso_cierto_list'),
#     path('egreso_cierto/new/', egreso_cierto_create, name='egreso_cierto_create'),
#     path('egreso_cierto/edit/<int:pk>/', egreso_cierto_update, name='egreso_cierto_update'),
#     path('egreso_cierto/delete/<int:pk>/', egreso_cierto_delete, name='egreso_cierto_delete'),

#     path('egreso_presupuestado/', egreso_presupuestado_list, name='egreso_presupuestado_list'),
#     path('egreso_presupuestado/new/', egreso_presupuestado_create, name='egreso_presupuestado_create'),
#     path('egreso_presupuestado/edit/<int:pk>/', egreso_presupuestado_update, name='egreso_presupuestado_update'),
#     path('egreso_presupuestado/delete/<int:pk>/', egreso_presupuestado_delete, name='egreso_presupuestado_delete'),

#     path('presupuesto_mensual_fijo/', presupuesto_mensual_fijo_list, name='presupuesto_mensual_fijo_list'),
#     path('presupuesto_mensual_fijo/new/', presupuesto_mensual_fijo_create, name='presupuesto_mensual_fijo_create'),
#     path('presupuesto_mensual_fijo/edit/<int:pk>/', presupuesto_mensual_fijo_update, name='presupuesto_mensual_fijo_update'),
#     path('presupuesto_mensual_fijo/delete/<int:pk>/', presupuesto_mensual_fijo_delete, name='presupuesto_mensual_fijo_delete'),

#     path('ingreso_cierto/', ingreso_cierto_list, name='ingreso_cierto_list'),
#     path('ingreso_cierto/new/', ingreso_cierto_create, name='ingreso_cierto_create'),
#     path('ingreso_cierto/edit/<int:pk>/', ingreso_cierto_update, name='ingreso_cierto_update'),
#     path('ingreso_cierto/delete/<int:pk>/', ingreso_cierto_delete, name='ingreso_cierto_delete'),

#     path('ingreso_previsionado/', ingreso_previsionado_list, name='ingreso_previsionado_list'),
#     path('ingreso_previsionado/new/', ingreso_previsionado_create, name='ingreso_previsionado_create'),
#     path('ingreso_previsionado/edit/<int:pk>/', ingreso_previsionado_update, name='ingreso_previsionado_update'),
#     path('ingreso_previsionado/delete/<int:pk>/', ingreso_previsionado_delete, name='ingreso_previsionado_delete'),
