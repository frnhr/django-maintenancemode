from django.http import HttpResponse

def index(request):
    return HttpResponse('Rendered response page, index')

def ignored(request):
    return HttpResponse('Rendered response page, ignored')
