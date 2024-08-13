from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from .forms import MakeForm, YearForm, ModelForm, SegmentForm, CategoryForm, PartForm, PartPropertyForm, AplicationForm, AplicationPhotoForm, PartPropertyFormSet
from vehicles.models import Aplication, Make, Year, Model, Segment, Category, Part, PartProperty, AplicationPhoto
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
import json
from datetime import datetime

class MainView(LoginRequiredMixin, View):
    def get(self, request):
        mc = Make.objects.count()
        yc = Year.objects.count()
        mlc = Model.objects.count()
        sg = Segment.objects.count()
        al = Aplication.objects.all()

        aplication_list = []
        for aplication in al:
            aplication_list.append({
                'id': aplication.id,
                'created_at': aplication.created_at.isoformat(),
                'updated_at': aplication.updated_at.isoformat(),
                'created_by_id': aplication.created_by_id,
                'updated_by_id': aplication.updated_by_id,
                'make_name': aplication.make.make,
                'model_name': aplication.model.model,
                'segment_name': aplication.segment.segment,
                'year_name': aplication.year.year,
                'market_name': aplication.market,
            })

        aplication_form = AplicationForm()
        ctx = {
            'title': 'Aplication',
            'headers': json.dumps(['Segment', 'Make', 'Model', 'Year', 'Market']),
            'fields': json.dumps(['segment_name', 'make_name', 'model_name', 'year_name', 'market_name']),
            'object_list_json': json.dumps(aplication_list),
            'object_list': al,
            'form': aplication_form,
            'return_url': 'vehicles:all',
            'create_url': 'vehicles:aplication_create',
            'update_url': 'vehicles:aplication_update',
            'delete_url': 'vehicles:aplication_delete',
            'make_count': mc,
            'year_count': yc,
            'model_count': mlc,
            'segment_count': sg,
        }
        return render(request, 'vehicles/aplication_list.html', ctx)

class LoadMoreAplicationsView(LoginRequiredMixin, View):
    def get(self, request):
        offset = int(request.GET.get('offset', 0))
        limit = 10
        aplications = Aplication.objects.all()[offset:offset + limit]
        context = {'aplication_list': aplications}
        html = render_to_string('vehicles/aplication_rows.html', context)
        return JsonResponse({'html': html})

class SearchAplicationsView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q', '')
        print(f"Received search query: {query}")  # Added for debugging
        q_objects = Q(segment__icontains=query) | Q(make__icontains=query) | Q(model__icontains=query)

        try:
            year = int(query)
            q_objects |= Q(year=year)
        except ValueError:
            pass

        aplications = Aplication.objects.filter(q_objects)
        context = {'aplication_list': aplications}
        html = render_to_string('vehicles/aplication_rows.html', context)
        return JsonResponse({'html': html})

class MakeView(LoginRequiredMixin, View):
    def get(self, request):
        makes = Make.objects.all().order_by('make')
        make_list = []
        for make in makes:
            make_list.append({
                'id': make.id,
                'created_at': make.created_at.isoformat(),
                'updated_at': make.updated_at.isoformat(),
                'created_by_id': make.created_by_id,
                'updated_by_id': make.updated_by_id,
                'make': make.make,
            })
        make_form = MakeForm()
        ctx = {
            'title': 'Make',
            'headers': json.dumps(['Name']),
            'fields': json.dumps(['make']),
            'object_list_json': json.dumps(make_list),
            'object_list': makes,
            'form': make_form,
            'return_url': 'vehicles:all',
            'create_url': 'vehicles:make_create',
            'update_url': 'vehicles:make_update',
            'delete_url': 'vehicles:make_delete',
        }
        return render(request, 'vehicles/base_table_list.html', ctx)

class YearView(LoginRequiredMixin, View):
    def get(self, request):
        years = Year.objects.all().order_by('-year')
        year_list = []
        for year in years:
            year_list.append({
                'id': year.id,
                'created_at': year.created_at.isoformat(),
                'updated_at': year.updated_at.isoformat(),
                'created_by_id': year.created_by_id,
                'updated_by_id': year.updated_by_id,
                'year': year.year,
            })
        year_form = YearForm()
        ctx = {
            'title': 'Year',
            'headers': json.dumps(['Year']),
            'fields': json.dumps(['year']),
            'object_list_json': json.dumps(year_list),
            'object_list': years,
            'form': year_form,
            'return_url': 'vehicles:all',
            'create_url': 'vehicles:year_create',
            'update_url': 'vehicles:year_update',
            'delete_url': 'vehicles:year_delete',
        }
        return render(request, 'vehicles/base_table_list.html', ctx)

class ModelView(LoginRequiredMixin, View):
    def get(self, request):
        models = Model.objects.all().order_by('model')
        model_list = []
        for model in models:
            model_list.append({
                'id': model.id,
                'created_at': model.created_at.isoformat(),
                'updated_at': model.updated_at.isoformat(),
                'created_by_id': model.created_by_id,
                'updated_by_id': model.updated_by_id,
                'model': model.model,
            })
        model_form = ModelForm()
        ctx = {
            'title': 'Model',
            'headers': json.dumps(['Model']),
            'fields': json.dumps(['model']),
            'object_list_json': json.dumps(model_list),
            'object_list': models,
            'form': model_form,
            'return_url': 'vehicles:all',
            'create_url': 'vehicles:model_create',
            'update_url': 'vehicles:model_update',
            'delete_url': 'vehicles:model_delete',
        }
        return render(request, 'vehicles/base_table_list.html', ctx)

class SegmentView(LoginRequiredMixin, View):
    def get(self, request):
        segments = Segment.objects.all().order_by('segment')
        segment_list = []
        for segment in segments:
            segment_list.append({
                'id': segment.id,
                'created_at': segment.created_at.isoformat(),
                'updated_at': segment.updated_at.isoformat(),
                'created_by_id': segment.created_by_id,
                'updated_by_id': segment.updated_by_id,
                'segment': segment.segment,
            })
        segment_form = SegmentForm()
        ctx = {
            'title': 'Segment',
            'headers': json.dumps(['Segment']),
            'fields': json.dumps(['segment']),
            'object_list_json': json.dumps(segment_list),
            'object_list': segments,
            'form': segment_form,
            'return_url': 'vehicles:all',
            'create_url': 'vehicles:segment_create',
            'update_url': 'vehicles:segment_update',
            'delete_url': 'vehicles:segment_delete',
        }
        return render(request, 'vehicles/base_table_list.html', ctx)

class AplicationDetailView(DetailView):
    model = Aplication
    template_name = 'vehicles/aplication_detail.html'
    context_object_name = 'aplication'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AplicationPhotoForm()
        return context

class AplicationPhotoUploadView(FormView):
    form_class = AplicationPhotoForm
    template_name = 'vehicles/aplication_detail.html'

    def form_valid(self, form):
        aplication = get_object_or_404(Aplication, pk=self.kwargs['pk'])
        form.instance.aplication = aplication
        form.save()
        return redirect('vehicles:aplication_detail', pk=aplication.pk)

class AplicationPhotoDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        photo = get_object_or_404(AplicationPhoto, pk=pk)
        aplication_id = photo.aplication.id
        photo.delete()
        return redirect('vehicles:aplication_detail', pk=aplication_id)

# CRUD Views for MAKES
class MakeCreate(LoginRequiredMixin, CreateView):
    model = Make
    form_class = MakeForm
    success_url = reverse_lazy('vehicles:make_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class MakeUpdate(LoginRequiredMixin, UpdateView):
    model = Make
    form_class = MakeForm
    success_url = reverse_lazy('vehicles:make_list')
    template_name = 'vehicles/update_form_partial.html'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.get_form()
            context = {
                'form': form,
                'object': self.get_object()
            }
            html_form = render_to_string(self.template_name, context, request=request)
            return JsonResponse({'html_form': html_form})
        return super().get(request, *args, **kwargs)

class MakeDelete(LoginRequiredMixin, DeleteView):
    model = Make
    success_url = reverse_lazy('vehicles:make_list')

# CRUD Views for YEARS
class YearCreate(LoginRequiredMixin, CreateView):
    model = Year
    form_class = YearForm
    success_url = reverse_lazy('vehicles:year_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class YearUpdate(LoginRequiredMixin, UpdateView):
    model = Year
    form_class = YearForm
    success_url = reverse_lazy('vehicles:year_list')
    template_name = 'vehicles/update_form_partial.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'form_is_valid': True,
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            data = {
                'form_is_valid': False,
                'html_form': render_to_string(self.template_name, {'form': form}, request=self.request)
            }
            return JsonResponse(data)
        else:
            return response

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.get_form()
            context = {
                'form': form,
                'object': self.get_object()
            }
            html_form = render_to_string(self.template_name, context, request=request)
            return JsonResponse({'html_form': html_form})
        return super().get(request, *args, **kwargs)




class YearDelete(LoginRequiredMixin, DeleteView):
    model = Year
    success_url = reverse_lazy('vehicles:year_list')

# CRUD Views for MODELS
class ModelCreate(LoginRequiredMixin, CreateView):
    model = Model
    form_class = ModelForm
    success_url = reverse_lazy('vehicles:model_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class ModelUpdate(LoginRequiredMixin, UpdateView):
    model = Model
    form_class = ModelForm
    success_url = reverse_lazy('vehicles:model_list')
    template_name = 'vehicles/update_form_partial.html'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.get_form()
            context = {
                'form': form,
                'object': self.get_object()
            }
            html_form = render_to_string(self.template_name, context, request=request)
            return JsonResponse({'html_form': html_form})
        return super().get(request, *args, **kwargs)

class ModelDelete(LoginRequiredMixin, DeleteView):
    model = Model
    success_url = reverse_lazy('vehicles:model_list')

# CRUD Views for APPLICATIONS
class AplicationCreate(LoginRequiredMixin, CreateView):
    model = Aplication
    form_class = AplicationForm
    success_url = reverse_lazy('vehicles:all')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class AplicationUpdate(LoginRequiredMixin, UpdateView):
    model = Aplication
    form_class = AplicationForm
    success_url = reverse_lazy('vehicles:all')
    template_name = 'vehicles/update_form_partial.html'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.get_form()
            context = {
                'form': form,
                'object': self.get_object()
            }
            html_form = render_to_string(self.template_name, context, request=request)
            return JsonResponse({'html_form': html_form})
        return super().get(request, *args, **kwargs)
    
class AplicationDelete(LoginRequiredMixin, DeleteView):
    model = Aplication
    success_url = reverse_lazy('vehicles:all')

# CRUD Views for SEGMENTS
class SegmentCreate(LoginRequiredMixin, CreateView):
    model = Segment
    form_class = SegmentForm
    success_url = reverse_lazy('vehicles:segment_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class SegmentUpdate(LoginRequiredMixin, UpdateView):
    model = Segment
    form_class = SegmentForm
    success_url = reverse_lazy('vehicles:segment_list')
    template_name = 'vehicles/update_form_partial.html'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.get_form()
            context = {
                'form': form,
                'object': self.get_object()
            }
            html_form = render_to_string(self.template_name, context, request=request)
            return JsonResponse({'html_form': html_form})
        return super().get(request, *args, **kwargs)

class SegmentDelete(LoginRequiredMixin, DeleteView):
    model = Segment
    success_url = reverse_lazy('vehicles:segment_list')

# CRUD Views for CATEGORIES
class CategoryView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.filter(level=0).prefetch_related('children__children').order_by('category')
        category_form = CategoryForm()
        ctx = {
            'title': 'Category',
            'categories': categories,
            'form': category_form,
            'create_url': 'vehicles:category_create',
            'update_url': 'vehicles:category_update',
            'delete_url': 'vehicles:category_delete',
        }
        return render(request, 'vehicles/category_list.html', ctx)

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('vehicles:category_list')

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('vehicles:category_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('vehicles:category_list')
    template_name = 'vehicles/update_form_partial.html'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.get_form()
            context = {
                'form': form,
                'object': self.get_object()
            }
            html_form = render_to_string(self.template_name, context, request=request)
            return JsonResponse({'html_form': html_form})
        return super().get(request, *args, **kwargs)

class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('vehicles:category_list')

# CRUD Views for PARTS
class PartListView(LoginRequiredMixin, View):
    def get(self, request):
        parts = Part.objects.all()
        
        part_list = []
        for part in parts:
            properties = PartProperty.objects.filter(part=part)
            properties_list = []
            for prop in properties:
                properties_list.append({
                    'property': prop.property,
                    'value': prop.value
                })
            
            part_list.append({
                'id': part.id,
                'sku': part.sku,
                'name': part.name,
                'categories': ", ".join([cat.category for cat in part.categories.all()]),
                'applications': " | ".join([str(app) for app in part.applications.all()]),  # Usa el método __str__
                'properties': properties_list,
                'description': part.description,
            })

        part_form = PartForm()
        ctx = {
            'title': 'Part',
            'headers': json.dumps(['Sku','Name', 'Categories', 'Applications', 'Property', 'Value','Description']),
            'fields': json.dumps(['sku','name', 'categories', 'applications', 'properties', 'description']),
            'object_list_json': json.dumps(part_list),
            'object_list': parts,
            'form': part_form,
            'create_url': 'vehicles:part_create',
            'update_url': 'vehicles:part_update',
            'delete_url': 'vehicles:part_delete',
        }
        return render(request, 'vehicles/part_list.html', ctx)


class PartCreate(LoginRequiredMixin, View):
    def get(self, request):
        part_form = PartForm()
        part_property_formset = PartPropertyFormSet(queryset=PartProperty.objects.none())
        ctx = {
            'part_form': part_form,
            'part_property_formset': part_property_formset,
        }
        return render(request, 'vehicles/part_form.html', ctx)

    def post(self, request):
        part_form = PartForm(request.POST)
        part_property_formset = PartPropertyFormSet(request.POST)
        if part_form.is_valid() and part_property_formset.is_valid():
            part = part_form.save(commit=False)
            part.created_by = request.user
            part.updated_by = request.user
            part.save()

            # Guardar el formset
            part_properties = part_property_formset.save(commit=False)
            for property in part_properties:
                property.part = part
                property.save()
            return redirect('vehicles:part_list')
        ctx = {
            'part_form': part_form,
            'part_property_formset': part_property_formset,
        }
        return render(request, 'vehicles/part_form.html', ctx)

class PartUpdate(LoginRequiredMixin, View):
    def get(self, request, pk):
        part = get_object_or_404(Part, pk=pk)
        part_form = PartForm(instance=part)
        part_property_formset = PartPropertyFormSet(instance=part)
        ctx = {
            'part_form': part_form,
            'part_property_formset': part_property_formset,
        }
        return render(request, 'vehicles/part_form.html', ctx)

    def post(self, request, pk):
        part = get_object_or_404(Part, pk=pk)
        part_form = PartForm(request.POST, instance=part)
        part_property_formset = PartPropertyFormSet(request.POST, instance=part)
        if part_form.is_valid() and part_property_formset.is_valid():
            part = part_form.save(commit=False)
            part.updated_by = request.user
            part.save()

            # Guardar el formset
            part_properties = part_property_formset.save(commit=False)
            for property in part_properties:
                property.part = part
                property.save()
            return redirect('vehicles:part_list')
        ctx = {
            'part_form': part_form,
            'part_property_formset': part_property_formset,
        }
        return render(request, 'vehicles/part_form.html', ctx)



class PartDelete(LoginRequiredMixin, DeleteView):
    model = Part
    success_url = reverse_lazy('vehicles:part_list')


# ---------------------------------------- View de properties obsoletos"---------------------------
# # CRUD Views for PROPERTIES
# class PropertyView(LoginRequiredMixin, View):
#     def get(self, request):
#         properties = Property.objects.all().order_by('name')
#         property_list = []
#         for property in properties:
#             property_list.append({
#                 'id': property.id,
#                 'created_at': property.created_at.isoformat(),
#                 'updated_at': property.updated_at.isoformat(),
#                 'created_by_id': property.created_by_id,
#                 'updated_by_id': property.updated_by_id,
#                 'property': property.name,
#             })
#         property_form = PropertyForm()
#         ctx = {
#             'title': 'Property',
#             'headers': json.dumps(['Property']),
#             'fields': json.dumps(['property']),
#             'object_list_json': json.dumps(property_list),
#             'object_list': properties,
#             'form': property_form,
#             'return_url': 'vehicles:all',
#             'create_url': 'vehicles:property_create',
#             'update_url': 'vehicles:property_update',
#             'delete_url': 'vehicles:property_delete',
#         }
#         return render(request, 'vehicles/base_table_list.html', ctx)


#-----------------------VIEW de modelo "Property" Obsoleto--------------------------
# class PropertyCreate(LoginRequiredMixin, CreateView):
#     model = Property
#     form_class = PropertyForm
#     success_url = reverse_lazy('vehicles:property_list')

#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         form.instance.updated_by = self.request.user
#         return super().form_valid(form)

# class PropertyUpdate(LoginRequiredMixin, UpdateView):
#     model = Property
#     form_class = PropertyForm
#     success_url = reverse_lazy('vehicles:property_list')
#     template_name = 'vehicles/update_form_partial.html'

#     def form_valid(self, form):
#         form.instance.updated_by = self.request.user
#         return super().form_valid(form)

#     def get(self, request, *args, **kwargs):
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             form = self.get_form()
#             context = {
#                 'form': form,
#                 'object': self.get_object()
#             }
#             html_form = render_to_string(self.template_name, context, request=request)
#             return JsonResponse({'html_form': html_form})
#         return super().get(request, *args, **kwargs)

# class PropertyDelete(LoginRequiredMixin, DeleteView):
#     model = Property
#     success_url = reverse_lazy('vehicles:property_list')
#---------------------------------------------------------------------------------------------------------


