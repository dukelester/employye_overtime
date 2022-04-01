from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

def pageNotFound(request, exception, template_name='error404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response


def serverError(request, template_name='errors500.html'):
    response = render(request, template_name)
    response.status_code = 500
    return render(request, template_name)

@login_required(login_url='login')
def CalenderView(request):
    return render(request,'calendar.html')
@login_required(login_url='login')
def homepageView(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def addEmployView(request):
    return render(request, 'company.html')
@login_required(login_url='login')
def addDepartmentView(request):
    return render(request, 'departments.html')

@login_required(login_url='login')
def addEmployeeView(request):
    return render(request, 'employees.html')
@login_required(login_url='login')
def companySettingsView(request):
    return render(request, 'settings.html')