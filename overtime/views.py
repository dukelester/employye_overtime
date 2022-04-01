from django.shortcuts import render

# Create your views here.

def pageNotFound(request, exception, template_name='error404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response


def serverError(request, template_name='errors500.html'):
    response = render(request, template_name)
    response.status_code = 500
    return render(request, template_name)

def homepageView(request):
    return render(request, 'index.html')