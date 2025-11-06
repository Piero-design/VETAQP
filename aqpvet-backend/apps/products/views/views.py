from django.http import JsonResponse

def index(request):
    return JsonResponse({'mensaje': 'Bienvenido al módulo de products'})
