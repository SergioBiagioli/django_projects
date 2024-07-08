from django.shortcuts import render
from django.http import HttpResponse


def hello_view(request):
    # Obtener el valor actual de la cookie
    #oldval = request.COOKIES.get('dj4e_cookie', None)

    # Incrementar el contador de visitas
    count_visit = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = count_visit
    response = HttpResponse('view count=' + str(count_visit))
    response.set_cookie('dj4e_cookie', '8c448021', max_age=1000)  # Actualizo la Cookie


    if count_visit > 4:
        request.session['num_visits'] = 0
        response = HttpResponse('view count=' + str(count_visit))
        return response

    # Si el contador de visitas no supera el límite, simplemente mostrar la información
    return response

