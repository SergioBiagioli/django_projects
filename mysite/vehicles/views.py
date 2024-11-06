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
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse
from django.apps import apps
from django.db.models import CharField, ForeignKey, ManyToManyField, IntegerField
import logging
from django.db.models.functions import Cast







class AplicationList(LoginRequiredMixin, View):
    def get(self, request):
        # Usa select_related para cargar las relaciones de manera eficiente
        al = Aplication.objects.all().select_related('make', 'model', 'segment', 'year').order_by('-updated_at')
        paginator = Paginator(al, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        aplication_list = []
        for aplication in page_obj:
            aplication_list.append({
                'id': aplication.id,
                'created_at': aplication.created_at.isoformat(),
                'updated_at': aplication.updated_at.isoformat(),
                'created_by_id': aplication.created_by_id,
                'updated_by_id': aplication.updated_by_id,
                'make_name': aplication.make.make if aplication.make else 'N/A',
                'model_name': aplication.model.model if aplication.model else 'N/A',
                'segment_name': aplication.segment.segment if aplication.segment else 'N/A',
                'year_name': aplication.year.year if aplication.year else 'N/A',
                'market_name': aplication.get_market_display(),  # Para mostrar el valor legible de market
            })

        aplication_form = AplicationForm()
        ctx = {
            'title': 'Aplication',
            'headers': ['Segment', 'Make', 'Model', 'Year', 'Market'],
            'fields': ['segment_name', 'make_name', 'model_name', 'year_name', 'market_name'],
            'object_list': page_obj,
            'form': aplication_form,
            'aplications' : aplication_list,
            'return_url': 'vehicles:all',
            'create_url': 'vehicles:aplication_create',
            'update_url': 'vehicles:aplication_update',
            'delete_url': 'vehicles:aplication_delete',
            'page_obj': page_obj,
            'show_search_bar': True,
            'has_detail_page' : True,
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
    
# Configurar un logger
logger = logging.getLogger(__name__)

def ajax_search_view(request):
    try:
        query = request.GET.get('query', '').strip()
        model_type = request.GET.get('model_type')
        
        if len(query) < 3:
            return JsonResponse({'results': [], 'total_results': 0})
        
        # Obtener el modelo dinámicamente
        try:
            model = apps.get_model('vehicles', model_type.capitalize())
            searchable_fields = getattr(model, 'searchable_fields', [])  # Obtiene los campos de búsqueda
        except LookupError:
            return JsonResponse({'results': [], 'total_results': 0, 'error': 'Modelo no encontrado'}, status=404)

        # Inicializamos el QuerySet
        queryset = model.objects.all()
        
        # Construcción del query `Q`
        search_terms = query.split()
        q_objects = Q()
        
        for term in search_terms:
            term_q = Q()
            for field in searchable_fields:
                field_object = model._meta.get_field(field)
                
                if isinstance(field_object, CharField):
                    # Aplica icontains solo a CharField
                    term_q |= Q(**{f"{field}__icontains": term})
                elif isinstance(field_object, ForeignKey):
                    # Para ForeignKey, busca un IntegerField o CharField en el modelo relacionado
                    related_model = field_object.related_model
                    related_integer_field = next(
                        (f.name for f in related_model._meta.get_fields() if isinstance(f, IntegerField) and f.name == 'year'), 
                        None
                    )
                    if related_integer_field:
                        # Anotamos el IntegerField del modelo relacionado (como 'year') como texto y aplicamos icontains
                        annotated_field = f"{field}__{related_integer_field}_as_text"
                        queryset = queryset.annotate(**{annotated_field: Cast(f"{field}__{related_integer_field}", CharField())})
                        term_q |= Q(**{f"{annotated_field}__icontains": term})
                    else:
                        # Si el modelo relacionado tiene CharField, aplica icontains en el campo relacionado de tipo CharField
                        related_char_field = next(
                            (f.name for f in related_model._meta.get_fields() if isinstance(f, CharField)), 
                            None
                        )
                        if related_char_field:
                            term_q |= Q(**{f"{field}__{related_char_field}__icontains": term})
                elif isinstance(field_object, IntegerField):
                    # Anotamos el campo IntegerField como texto y aplicamos icontains en el campo anotado
                    annotated_field = f"{field}_as_text"
                    queryset = queryset.annotate(**{annotated_field: Cast(field, CharField())})
                    term_q |= Q(**{f"{annotated_field}__icontains": term})

            q_objects &= term_q

        queryset = queryset.filter(q_objects).distinct()
        results = queryset[:3]
        total_results = queryset.count()

        result_list = [{'id': obj.id, 'text': str(obj)} for obj in results]
        
        return JsonResponse({
            'results': result_list,
            'total_results': total_results
        })
        
    except Exception as e:
        return JsonResponse({'results': [], 'total_results': 0, 'error': str(e)}, status=500)



    
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
    template_name = 'vehicles/modal.html'

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


from django.db.models import Q
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Part
from .forms import PartForm

class PartListView(LoginRequiredMixin, View):

    def get(self, request):
        strval = request.GET.get('search_here', '')

        if strval:
            query = Q(sku__icontains=strval)
            query.add(Q(name__icontains=strval), Q.OR)
            query.add(Q(categories__category__icontains=strval), Q.OR)
            query.add(Q(applications__segment__segment__icontains=strval), Q.OR)
            query.add(Q(applications__make__make__icontains=strval), Q.OR)
            query.add(Q(applications__year__year__icontains=strval), Q.OR)
            query.add(Q(applications__model__model__icontains=strval), Q.OR)
            query.add(Q(applications__market__icontains=strval), Q.OR)
            query.add(Q(notes__icontains=strval), Q.OR)
            parts = Part.objects.filter(query).select_related(
                'categories', 
                'applications__segment',
                'applications__make',
                'applications__year', 
                'applications__model'
            ).prefetch_related('categories', 
                               'applications').distinct().only(
                                'sku', 
                                'name', 
                                'categories', 
                                'applications', 
                                'notes', 
                                'description'
            ).order_by('sku')
        else:
            # Define 'parts' con todos los objetos si no hay búsqueda
            parts = Part.objects.all().only(
                'sku', 
                'name', 
                'categories', 
                'applications', 
                'notes', 
                'description'
            ).order_by('sku')

        paginator = Paginator(parts, 20)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        part_form = PartForm()
        ctx = {
            'title': 'Part',
            'headers': ['Sku',  'Categories', 'Applications', 'Property', 'Notes', 'Description'],
            'fields': ['sku',  'categories', 'applications', 'properties', 'notes', 'description'],
            'object_list': page_obj,
            'form': part_form,
            'search_here': strval,
            'create_url': 'vehicles:part_create',
            'update_url': 'vehicles:part_update',
            'delete_url': 'vehicles:part_delete',
            'page_obj': page_obj,
            'show_search_bar': True,
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


