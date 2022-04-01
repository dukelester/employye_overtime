from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
from . models import Company
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
    if request.method == 'POST':
        my_company = Company (
            company_name = request.POST.get('company_name'),
            contact_person = request.POST.get('contact_person'),
            company_email = request.POST.get('company_email'),
            description = request.POST.get('description'),
            address = request.POST.get('address'),
            country = request.POST.get('country'),
            city = request.POST.get('city'),
            town = request.POST.get('town'),
            postal_code = request.POST.get('postal_code'),
            phone_number = request.POST.get('phone_number'),
            office_number = request.POST.get('office_number'),
            fax = request.POST.get('fax'),
            website_url = request.POST.get('website_url'),
            
        )
        
        my_company.save()
        print("company details added successfully")
        messages.add_message(request, messages.SUCCESS, "Company Details Updated Successfully")
        
        if my_company:
            return redirect('homepage')
        
        
        return render(request, 'settings.html')
    else:
        company = Company.objects.all().order_by('-created_at').first()
        print(company, 'asdfghjkl;lkjhgfdsdfghj')
        
        return render(request, 'settings.html', {'company':company})