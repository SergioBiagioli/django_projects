from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
from vehicles.models import Aplication

def search(request):
    query = request.GET.get('q', '')
    words = query.split()
    q_objects = Q()
    for word in words:
        q_objects &= (Q(segment__icontains=word) | Q(make__icontains=word) | Q(year__icontains=word) | Q(model__icontains=word))

    aplications = Aplication.objects.filter(q_objects)
    context = {'aplication_list': aplications}
    html = render_to_string('vehicles/aplication_rows.html', context)
    return JsonResponse({'html': html})
