from django.contrib import admin
from .models import Company, Departments, Employee,Overtime
# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'company_email', 'description',
                    'address','postal_code','country','city', 'town','phone_number', 'office_number', 'fax', 'website_url')
    search_fields = ('company_name', 'company_email', 'phone_number','office_number','fax')
    readonly_fields = ('id', 'created_at')


admin.site.register(Company,CompanyAdmin)

class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('company', 'department_name', 'number_of_employees', 'minimum_salary', 'maximum_salary', 'overtime_pay_perhour')
    search_fields = ('department_name', 'number_of_employees',)
    readonly_fields = ('id', 'created_at', 'updated_at')

admin.site.register(Departments,DepartmentsAdmin)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'phone', 'username', 'email', 'employee','address')
    search_fields = ('last_name', 'first_name', 'phone',)
    readonly_fields = ('id', 'created_at', 'updated_at')


admin.site.register(Employee,EmployeeAdmin)

class OvertimeAdmin(admin.ModelAdmin):
    list_display = ('description', 'overtime_hours', 'overtime_pay', 'overtime_date')
    search_fields = ('overtime_pay', 'description',)
    readonly_fields = ('id', 'created_at')

admin.site.register(Overtime,OvertimeAdmin)