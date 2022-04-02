from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import Account
from django.db.models import Sum
from authentication.views import send_activation_email
# Create your views here.
from . models import Company,Departments, Employee, Overtime
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
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
    #data view 
    context = {}
    departments = Departments.objects.all()
    context['departments'] = departments.count()
    context['employees'] = Employee.objects.all().count()
    hours = Overtime.objects.filter(approved_by=request.user).aggregate(Sum("overtime_hours"))
    total_overtime = Overtime.objects.filter(approved_by=request.user).aggregate(Sum("total"))
    print(hours, 'hhhhhhhhhhhhhhhhhhhh',total_overtime)
    context['overtime_hours'] = hours['overtime_hours__sum']
    context['total_overtime'] = total_overtime['total__sum']
    
    return render(request, 'index.html', context)

@login_required(login_url='login')
def addEmployView(request):
    return render(request, 'company.html')
@login_required(login_url='login')
def addDepartmentView(request):
    context = {}
    context['company'] = Company.objects.all()
    departments = Departments.objects.all()
    
    context['departments'] = departments
    if request.method == 'POST':
        department = Departments(
            company = request.POST.get('company'),
            department_name = request.POST.get('department_name'),
            number_of_employees = request.POST.get('number_of_employees'),
            minimum_salary = request.POST.get('minimum_salary'),
            maximum_salary = request.POST.get('maximum_salary'),
            overtime_pay_perhour = request.POST.get('overtime_pay_perhour'),
            
        )
        department.save()
        messages.add_message(request, messages.SUCCESS, "Company Details Updated Successfully")
        
        if department:
            return redirect('departments')
            
            
    
    return render(request, 'departments.html', context)

@login_required(login_url='login')
def addEmployeeView(request):
    context = {}
    companies = Company.objects.all()
    departments = Departments.objects.all()
    context['companies'] = companies
    context['departments'] = departments
    context['employees'] = Employee.objects.all()
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        
        phone_exists = User.objects.filter(phone=phone).exists()
        email_exist = User.objects.filter(email=email).exists()
        username_exist = User.objects.filter(username=username).exists()
        if phone_exists:
            messages.add_message(
            request, messages.ERROR, "The Phone Has Been Taken!")
            return render(request, 'employees.html', context)
        if email_exist:
            messages.add_message(
            request, messages.ERROR, "The Email Has Been Taken!")
            return render(request, 'employees.html', context)
        if username_exist:
            messages.add_message(
            request, messages.ERROR, "The Username Has Been Taken!")
            return render(request, 'employees.html', context)
        new_employee = Employee (
            company = request.POST.get('company'),
            department = request.POST.get('department'),
            employee = User.objects.create_user(
                email=email, username=email, phone=phone,password="Employee2022"),
            # email = request.POST.get('email'),
            # username = request.POST.get('username'),
            # phone = request.POST.get('phone'),
            mobile = request.POST.get('mobile'),
            address = request.POST.get('address'),
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            employeeReg_Id = request.POST.get('employeeReg_Id'),
        )
        new_employee.email = email
        new_employee.username = username
        new_employee.phone = phone
        new_employee.is_email_verified = True
        new_employee.save()
        
        # emp_account = Account.objects.get(username=new_employee.username)
        # emp_account.is_email_verified = True
        # emp_account.save()
        print("employee details added successfully")
        #send the email for password and user name
        send_activation_email(new_employee, request) #activation email
        print('acvtivation sent')
  
        
        messages.add_message(request, messages.SUCCESS, "Employee Details Added Successfully")
        
    return render(request, 'employees.html', context)
@login_required(login_url='login')
def companySettingsView(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        get_company = Company.objects.get(company_name=company_name)
        print(get_company, 'gotttttttttttttt')
        my_company = Company (
            company_name = get_company,
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
    

@login_required(login_url='login')
def addOverTimeView(request):
    context = {}
    context['overtime'] = Overtime.objects.all()
    context['employees'] = Employee.objects.all()
    if request.method == 'POST':
        my_employee = request.POST.get('my_employee')
        overtime_date = request.POST.get('overtime_date')
        overtime_hours = request.POST.get('overtime_hours')
        description = request.POST.get('description')
        overtime_type = request.POST.get('overtime_type')
        overtime_pay = request.POST.get('overtime_pay')
        total = request.POST.get('total')
        
        # print(my_employee, 'empppppppppppp')
        my_emp = Employee.objects.get(email=my_employee)
        
        new_overtime = Overtime(
            my_employee = my_emp,
            overtime_date =overtime_date,
            overtime_hours = overtime_hours,
            description = description,
            overtime_type = overtime_type,
            overtime_pay = overtime_pay,
            approved_by = request.user

        )
        #total
        total = int(overtime_pay) * int(overtime_hours)
        new_overtime.total = total
        new_overtime.save()
    return render(request, 'overtime.html', context)