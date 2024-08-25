from django.views import View
from django.shortcuts import render

class ShowText(View):
    template_name = 'form.html'

    def get(self, request):
        # Muestra el formulario vacío inicialmente
        return render(request, self.template_name)

    def post(self, request):
        # Captura los valores de los campos enviados por el formulario
        txt_1 = request.POST.get('campo1', '').strip()
        txt_2 = request.POST.get('campo2', '').strip()

        # Concatenar los textos con un espacio en el medio y convertir a mayúsculas
        result = f"{txt_1} {txt_2}".upper()

        # Pasar el resultado a la plantilla para mostrarlo
        return render(request, self.template_name, {'result': result})
