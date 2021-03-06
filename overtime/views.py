from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import Account
from django.db.models import Sum
from authentication.views import send_activation_email
# Create your views here.
from . models import Company,Departments, Employee, Overtime,RequestedOvertimes
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
def pageNotFound(request, exception, template_name='error-404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response


def serverError(request, template_name='error-500.html'):
    response = render(request, template_name)
    response.status_code = 500
    return render(request, template_name)

@login_required(login_url='login')
def CalenderView(request):
    return render(request,'calendar.html')
@login_required(login_url='login')
def homepageView(request):
    context = {}
    if not request.user.is_authenticated:
        messages.add_message(
        request, messages.SUCCESS, "Welcome Guest User!")
        return render(request, 'index.html')
    elif request.user.is_hr:
        #data view 
        departments = Departments.objects.filter(Hr=request.user)
        context['departments'] = departments.count()
        context['employees'] = Employee.objects.filter(Hr=request.user).count()
        hours = Overtime.objects.filter(approved_by=request.user).aggregate(Sum("overtime_hours"))
        total_overtime = Overtime.objects.filter(approved_by=request.user).aggregate(Sum("total"))
        print(hours, 'hhhhhhhhhhhhhhhhhhhh',total_overtime)
        context['overtime_hours'] = hours['overtime_hours__sum']
        context['total_overtime'] = total_overtime['total__sum']
        
   
        return render(request, 'index.html', context)
    else:
        try:
            context = {}
            emp = Employee.objects.get(employee=request.user)
           
            context['first_name'] =emp.first_name
            context['last_name'] =emp.last_name
            my_overtime_hours =  Overtime.objects.filter(my_employee=emp).latest('created_at')
            context['my_overtime_hours'] = my_overtime_hours.overtime_hours
            my_total_overtime =  Overtime.objects.filter(my_employee=emp).latest('created_at')
            context['my_total_overtime'] = my_total_overtime.total
            total_earnings =  Overtime.objects.filter(my_employee=emp).aggregate(Sum("total"))
            context['total_earnings'] = total_earnings['total__sum']
            my_day =  Overtime.objects.filter(my_employee=emp).latest('created_at')
            context['my_day'] = my_day.overtime_date
            approved_by = Overtime.objects.filter(my_employee=emp).latest('created_at')
            context['approved_by'] = my_day.approved_by
            print(emp, 'meeeeeeeeeeeeeeeeeee',my_overtime_hours,my_total_overtime,my_day)
            
            context['overtime'] = Overtime.objects.filter(my_employee=emp).all()
            
            return render(request, 'index.html', context)
        except:
            return render(request, 'index.html', context)

@login_required(login_url='login')
def addEmployView(request):
    return render(request, 'company.html')
@login_required(login_url='login')
def addDepartmentView(request):
    if request.user.is_hr:
        context = {}
        context['company'] = Company.objects.all()
        departments = Departments.objects.filter(Hr=request.user)
        
        context['departments'] = departments
        if request.method == 'POST':
            department = Departments(
                company = request.POST.get('company'),
                department_name = request.POST.get('department_name'),
                number_of_employees = request.POST.get('number_of_employees'),
                minimum_salary = request.POST.get('minimum_salary'),
                maximum_salary = request.POST.get('maximum_salary'),
                overtime_pay_perhour = request.POST.get('overtime_pay_perhour'),
                Hr=request.user
                
            )
            department.save()
            messages.add_message(request, messages.SUCCESS, "Company Details Updated Successfully")
            
            if department:
                return redirect('departments')
                
        return render(request, 'departments.html', context)
    else:
        return render(request, 'error-403.html')

@login_required(login_url='login')
def addEmployeeView(request):
    if request.user.is_hr:
        context = {}
        companies = Company.objects.all()
        departments = Departments.objects.filter(Hr=request.user)
        context['companies'] = companies
        context['departments'] = departments
        context['employees'] = Employee.objects.filter(Hr=request.user).order_by('-created_at')
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
                Hr = request.user,
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
    else:
        return render(request, 'error-403.html')
@login_required(login_url='login')
def companySettingsView(request):
    if request.user.is_hr:
        if request.method == 'POST':
            my_company = Company (
                Hr = request.user,
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
            company = Company.objects.filter(Hr=request.user).order_by('-created_at').first()
            print(company, 'asdfghjkl;lkjhgfdsdfghj')
            
            return render(request, 'settings.html', {'company':company})
    else:
        return render(request, 'error-403.html')

@login_required(login_url='login')
def addOverTimeView(request):
    if request.user.is_hr:
        context = {}
        context['overtime'] = Overtime.objects.filter(approved_by=request.user).order_by('-created_at')
        context['employees'] = Employee.objects.filter(Hr=request.user).order_by('-created_at')

        get_employees_request = RequestedOvertimes.objects.all()
        context['requested_overtimes'] = get_employees_request

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
            messages.add_message(request, messages.SUCCESS, "Overtime Details added Successfully")
        return render(request, 'overtime.html', context)
    else:
        return render(request, 'error-403.html')


def requestForOvertime(request):
    context = {}
    employee = request.user
    my_employer = Employee.objects.get(employee=employee)
    print(my_employer.Hr)

    my_requested_overtimes = RequestedOvertimes.objects.filter(employee=request.user).order_by('-requested_at').all()  
    context['my_overtimes'] = my_requested_overtimes
    context['departments'] = Departments.objects.all()
    
    if request.method=='POST':
        employer=my_employer.Hr
        employee = request.user
        overtime_date = request.POST.get('overtime_date')
        overtime_hours = request.POST.get('overtime_hours')
        description = request.POST.get('description')
        overtime_type = request.POST.get('overtime_type')

        
        requested_overtime = RequestedOvertimes(
            employer=my_employer.Hr,
            employee = request.user,
            overtime_date =overtime_date,
            overtime_hours = overtime_hours,
            description = description,
            overtime_type = overtime_type,
         
        )
        requested_overtime.save()
        messages.add_message(request, messages.SUCCESS, "Overtime Requested Successfully")
    return render(request, 'requestovertime.html', context)

def approveNow(request, pk):
    my_overtime = RequestedOvertimes.objects.get(id=pk)
    print(my_overtime)
    if request.method == 'POST':
        my_overtime.approved = True
        my_overtime.save()
        messages.add_message(request, messages.SUCCESS, "Overtime Approved Successfully")

    return redirect('overTime')
