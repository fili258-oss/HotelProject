from django.shortcuts import render

def home(request):
    """
    Vista para la página de inicio del sitio.
    """
    # Puedes pasar variables al contexto si las necesitas
    context = {
        'page_title': 'Inicio',
    }
    return render(request, 'core/home.html', context)