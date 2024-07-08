from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from .models import Empresa, Sucursal, EgresoCierto, EgresoPresupuestado, PresupuestoMensualFijo, IngresoCierto, IngresoPrevisionado
from .forms import EmpresaForm, SucursalForm, EgresoCiertoForm, EgresoPresupuestadoForm, PresupuestoMensualFijoForm, IngresoCiertoForm, IngresoPrevisionadoForm
from django.core.serializers.json import DjangoJSONEncoder
import json

class EmpresaListView(LoginRequiredMixin, View):
    def get(self, request):
        empresas = Empresa.objects.all()
        fields = ['nombre', 'direccion', 'telefono', 'email']
        headers = ['Nombre', 'Dirección', 'Teléfono', 'Email']
        object_list_json = json.dumps(list(empresas.values(*fields)), cls=DjangoJSONEncoder)
        headers_json = json.dumps(headers)
        fields_json = json.dumps(fields)
        return render(request, 'empresa_list.html', {
            'title': 'Empresa',
            'object_list': empresas,
            'object_list_json': object_list_json,
            'fields_json': fields_json,
            'headers_json': headers_json,
            'update_url': 'cashmanagement:empresa_update',
            'delete_url': 'cashmanagement:empresa_delete',
            'create_url': 'cashmanagement:empresa_create',
            'return_url': 'cashmanagement:empresa_list',
            'form': EmpresaForm()
        })
# Repeat for other views


class SucursalListView(LoginRequiredMixin, View):
    def get(self, request):
        sucursales = Sucursal.objects.all()
        fields = ['nombre', 'direccion', 'telefono', 'email', 'empresa']
        headers = ['Nombre', 'Dirección', 'Teléfono', 'Email', 'Empresa']
        object_list_json = json.dumps(list(sucursales.values(*fields)), cls=DjangoJSONEncoder)
        return render(request, 'base_table.html', {
            'title': 'Sucursal',
            'object_list': sucursales,
            'object_list_json': object_list_json,
            'fields': fields,
            'headers': headers,
            'update_url': 'cashmanagement:sucursal_update',
            'delete_url': 'cashmanagement:sucursal_delete',
            'create_url': 'cashmanagement:sucursal_create',
            'form': SucursalForm()
        })

class EgresoCiertoListView(LoginRequiredMixin, View):
    def get(self, request):
        egresos = EgresoCierto.objects.all()
        fields = ['fecha', 'fecha_vencimiento', 'proveedor_cliente', 'modalidad', 'importe_total', 'importe_pagado', 'importe_adeudado', 'sucursal']
        headers = ['Fecha', 'Fecha Vencimiento', 'Proveedor/Cliente', 'Modalidad', 'Importe Total', 'Importe Pagado', 'Importe Adeudado', 'Sucursal']
        object_list_json = json.dumps(list(egresos.values(*fields)), cls=DjangoJSONEncoder)
        return render(request, 'base_table.html', {
            'title': 'EgresoCierto',
            'object_list': egresos,
            'object_list_json': object_list_json,
            'fields': fields,
            'headers': headers,
            'update_url': 'cashmanagement:egreso_cierto_update',
            'delete_url': 'cashmanagement:egreso_cierto_delete',
            'create_url': 'cashmanagement:egreso_cierto_create',
            'form': EgresoCiertoForm()
        })

class EgresoPresupuestadoListView(LoginRequiredMixin, View):
    def get(self, request):
        egresos = EgresoPresupuestado.objects.all()
        fields = ['fecha', 'fecha_vencimiento', 'proveedor_cliente', 'modalidad', 'importe_total', 'importe_pagado', 'importe_adeudado', 'sucursal']
        headers = ['Fecha', 'Fecha Vencimiento', 'Proveedor/Cliente', 'Modalidad', 'Importe Total', 'Importe Pagado', 'Importe Adeudado', 'Sucursal']
        object_list_json = json.dumps(list(egresos.values(*fields)), cls=DjangoJSONEncoder)
        return render(request, 'base_table.html', {
            'title': 'EgresoPresupuestado',
            'object_list': egresos,
            'object_list_json': object_list_json,
            'fields': fields,
            'headers': headers,
            'update_url': 'cashmanagement:egreso_presupuestado_update',
            'delete_url': 'cashmanagement:egreso_presupuestado_delete',
            'create_url': 'cashmanagement:egreso_presupuestado_create',
            'form': EgresoPresupuestadoForm()
        })

class PresupuestoMensualFijoListView(LoginRequiredMixin, View):
    def get(self, request):
        presupuestos = PresupuestoMensualFijo.objects.all()
        fields = ['fecha', 'fecha_vencimiento', 'proveedor', 'modalidad', 'importe_total', 'categoria', 'sucursal']
        headers = ['Fecha', 'Fecha Vencimiento', 'Proveedor', 'Modalidad', 'Importe Total', 'Categoría', 'Sucursal']
        object_list_json = json.dumps(list(presupuestos.values(*fields)), cls=DjangoJSONEncoder)
        return render(request, 'base_table.html', {
            'title': 'PresupuestoMensualFijo',
            'object_list': presupuestos,
            'object_list_json': object_list_json,
            'fields': fields,
            'headers': headers,
            'update_url': 'cashmanagement:presupuesto_mensual_fijo_update',
            'delete_url': 'cashmanagement:presupuesto_mensual_fijo_delete',
            'create_url': 'cashmanagement:presupuesto_mensual_fijo_create',
            'form': PresupuestoMensualFijoForm()
        })

class IngresoCiertoListView(LoginRequiredMixin, View):
    def get(self, request):
        ingresos = IngresoCierto.objects.all()
        fields = ['fecha', 'fecha_vencimiento', 'proveedor_cliente', 'modalidad', 'importe_total', 'importe_pagado', 'importe_adeudado', 'sucursal']
        headers = ['Fecha', 'Fecha Vencimiento', 'Proveedor/Cliente', 'Modalidad', 'Importe Total', 'Importe Pagado', 'Importe Adeudado', 'Sucursal']
        object_list_json = json.dumps(list(ingresos.values(*fields)), cls=DjangoJSONEncoder)
        return render(request, 'base_table.html', {
            'title': 'IngresoCierto',
            'object_list': ingresos,
            'object_list_json': object_list_json,
            'fields': fields,
            'headers': headers,
            'update_url': 'cashmanagement:ingreso_cierto_update',
            'delete_url': 'cashmanagement:ingreso_cierto_delete',
            'create_url': 'cashmanagement:ingreso_cierto_create',
            'form': IngresoCiertoForm()
        })

class IngresoPrevisionadoListView(LoginRequiredMixin, View):
    def get(self, request):
        ingresos = IngresoPrevisionado.objects.all()
        fields = ['fecha', 'fecha_vencimiento', 'proveedor_cliente', 'modalidad', 'importe_total', 'importe_pagado', 'importe_adeudado', 'sucursal']
        headers = ['Fecha', 'Fecha Vencimiento', 'Proveedor/Cliente', 'Modalidad', 'Importe Total', 'Importe Pagado', 'Importe Adeudado', 'Sucursal']
        object_list_json = json.dumps(list(ingresos.values(*fields)), cls=DjangoJSONEncoder)
        return render(request, 'base_table.html', {
            'title': 'IngresoPrevisionado',
            'object_list': ingresos,
            'object_list_json': object_list_json,
            'fields': fields,
            'headers': headers,
            'update_url': 'cashmanagement:ingreso_previsionado_update',
            'delete_url': 'cashmanagement:ingreso_previsionado_delete',
            'create_url': 'cashmanagement:ingreso_previsionado_create',
            'form': IngresoPrevisionadoForm()
        })

class EmpresaCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = EmpresaForm()
        return render(request, 'empresa_form.html', {'form': form})

    def post(self, request):
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:empresa_list')
        return render(request, 'empresa_form.html', {'form': form})

class EmpresaUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        empresa = get_object_or_404(Empresa, pk=pk)
        form = EmpresaForm(instance=empresa)
        return render(request, 'empresa_form.html', {'form': form})

    def post(self, request, pk):
        empresa = get_object_or_404(Empresa, pk=pk)
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:empresa_list')
        return render(request, 'empresa_form.html', {'form': form})

class EmpresaDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        empresa = get_object_or_404(Empresa, pk=pk)
        return render(request, 'empresa_confirm_delete.html', {'empresa': empresa})

    def post(self, request, pk):
        empresa = get_object_or_404(Empresa, pk=pk)
        empresa.delete()
        return redirect('cashmanagement:empresa_list')

class SucursalCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = SucursalForm()
        return render(request, 'sucursal_form.html', {'form': form})

    def post(self, request):
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:sucursal_list')
        return render(request, 'sucursal_form.html', {'form': form})

class SucursalUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        sucursal = get_object_or_404(Sucursal, pk=pk)
        form = SucursalForm(instance=sucursal)
        return render(request, 'sucursal_form.html', {'form': form})

    def post(self, request, pk):
        sucursal = get_object_or_404(Sucursal, pk=pk)
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:sucursal_list')
        return render(request, 'sucursal_form.html', {'form': form})

class SucursalDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        sucursal = get_object_or_404(Sucursal, pk=pk)
        return render(request, 'sucursal_confirm_delete.html', {'sucursal': sucursal})

    def post(self, request, pk):
        sucursal = get_object_or_404(Sucursal, pk=pk)
        sucursal.delete()
        return redirect('cashmanagement:sucursal_list')

class EgresoCiertoCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = EgresoCiertoForm()
        return render(request, 'egreso_cierto_form.html', {'form': form})

    def post(self, request):
        form = EgresoCiertoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:egreso_cierto_list')
        return render(request, 'egreso_cierto_form.html', {'form': form})

class EgresoCiertoUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        egreso = get_object_or_404(EgresoCierto, pk=pk)
        form = EgresoCiertoForm(instance=egreso)
        return render(request, 'egreso_cierto_form.html', {'form': form})

    def post(self, request, pk):
        egreso = get_object_or_404(EgresoCierto, pk=pk)
        form = EgresoCiertoForm(request.POST, instance=egreso)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:egreso_cierto_list')
        return render(request, 'egreso_cierto_form.html', {'form': form})

class EgresoCiertoDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        egreso = get_object_or_404(EgresoCierto, pk=pk)
        return render(request, 'egreso_cierto_confirm_delete.html', {'egreso': egreso})

    def post(self, request, pk):
        egreso = get_object_or_404(EgresoCierto, pk=pk)
        egreso.delete()
        return redirect('cashmanagement:egreso_cierto_list')

class EgresoPresupuestadoCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = EgresoPresupuestadoForm()
        return render(request, 'egreso_presupuestado_form.html', {'form': form})

    def post(self, request):
        form = EgresoPresupuestadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:egreso_presupuestado_list')
        return render(request, 'egreso_presupuestado_form.html', {'form': form})

class EgresoPresupuestadoUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        egreso = get_object_or_404(EgresoPresupuestado, pk=pk)
        form = EgresoPresupuestadoForm(instance=egreso)
        return render(request, 'egreso_presupuestado_form.html', {'form': form})

    def post(self, request, pk):
        egreso = get_object_or_404(EgresoPresupuestado, pk=pk)
        form = EgresoPresupuestadoForm(request.POST, instance=egreso)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:egreso_presupuestado_list')
        return render(request, 'egreso_presupuestado_form.html', {'form': form})

class EgresoPresupuestadoDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        egreso = get_object_or_404(EgresoPresupuestado, pk=pk)
        return render(request, 'egreso_presupuestado_confirm_delete.html', {'egreso': egreso})

    def post(self, request, pk):
        egreso = get_object_or_404(EgresoPresupuestado, pk=pk)
        egreso.delete()
        return redirect('cashmanagement:egreso_presupuestado_list')

class PresupuestoMensualFijoCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = PresupuestoMensualFijoForm()
        return render(request, 'presupuesto_mensual_fijo_form.html', {'form': form})

    def post(self, request):
        form = PresupuestoMensualFijoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:presupuesto_mensual_fijo_list')
        return render(request, 'presupuesto_mensual_fijo_form.html', {'form': form})

class PresupuestoMensualFijoUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        presupuesto = get_object_or_404(PresupuestoMensualFijo, pk=pk)
        form = PresupuestoMensualFijoForm(instance=presupuesto)
        return render(request, 'presupuesto_mensual_fijo_form.html', {'form': form})

    def post(self, request, pk):
        presupuesto = get_object_or_404(PresupuestoMensualFijo, pk=pk)
        form = PresupuestoMensualFijoForm(request.POST, instance=presupuesto)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:presupuesto_mensual_fijo_list')
        return render(request, 'presupuesto_mensual_fijo_form.html', {'form': form})

class PresupuestoMensualFijoDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        presupuesto = get_object_or_404(PresupuestoMensualFijo, pk=pk)
        return render(request, 'presupuesto_mensual_fijo_confirm_delete.html', {'presupuesto': presupuesto})

    def post(self, request, pk):
        presupuesto = get_object_or_404(PresupuestoMensualFijo, pk=pk)
        presupuesto.delete()
        return redirect('cashmanagement:presupuesto_mensual_fijo_list')

class IngresoCiertoCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = IngresoCiertoForm()
        return render(request, 'ingreso_cierto_form.html', {'form': form})

    def post(self, request):
        form = IngresoCiertoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:ingreso_cierto_list')
        return render(request, 'ingreso_cierto_form.html', {'form': form})

class IngresoCiertoUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        ingreso = get_object_or_404(IngresoCierto, pk=pk)
        form = IngresoCiertoForm(instance=ingreso)
        return render(request, 'ingreso_cierto_form.html', {'form': form})

    def post(self, request, pk):
        ingreso = get_object_or_404(IngresoCierto, pk=pk)
        form = IngresoCiertoForm(request.POST, instance=ingreso)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:ingreso_cierto_list')
        return render(request, 'ingreso_cierto_form.html', {'form': form})

class IngresoCiertoDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        ingreso = get_object_or_404(IngresoCierto, pk=pk)
        return render(request, 'ingreso_cierto_confirm_delete.html', {'ingreso': ingreso})

    def post(self, request, pk):
        ingreso = get_object_or_404(IngresoCierto, pk=pk)
        ingreso.delete()
        return redirect('cashmanagement:ingreso_cierto_list')

class IngresoPrevisionadoCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = IngresoPrevisionadoForm()
        return render(request, 'ingreso_previsionado_form.html', {'form': form})

    def post(self, request):
        form = IngresoPrevisionadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:ingreso_previsionado_list')
        return render(request, 'ingreso_previsionado_form.html', {'form': form})

class IngresoPrevisionadoUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        ingreso = get_object_or_404(IngresoPrevisionado, pk=pk)
        form = IngresoPrevisionadoForm(instance=ingreso)
        return render(request, 'ingreso_previsionado_form.html', {'form': form})

    def post(self, request, pk):
        ingreso = get_object_or_404(IngresoPrevisionado, pk=pk)
        form = IngresoPrevisionadoForm(request.POST, instance=ingreso)
        if form.is_valid():
            form.save()
            return redirect('cashmanagement:ingreso_previsionado_list')
        return render(request, 'ingreso_previsionado_form.html', {'form': form})

class IngresoPrevisionadoDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        ingreso = get_object_or_404(IngresoPrevisionado, pk=pk)
        return render(request, 'ingreso_previsionado_confirm_delete.html', {'ingreso': ingreso})

    def post(self, request, pk):
        ingreso = get_object_or_404(IngresoPrevisionado, pk=pk)
        ingreso.delete()
        return redirect('cashmanagement:ingreso_previsionado_list')
