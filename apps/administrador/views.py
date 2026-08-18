from django.shortcuts import render


def dashboard(request):
    contexto = {
        'titulo': 'Administración de la Finca',
    }

    return render(
        request,
        'administrador/dashboard.html',
        contexto,
    )
    
   
def indicadores(request):
    return render(request, "administrador/indicadores.html")