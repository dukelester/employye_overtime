from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
class Company(models.Model):
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    company_email = models.EmailField()
    description = models.TextField()
    address = models.TextField()
    country = models.CharField(max_length=255, default="Kenya")
    city = models.CharField(max_length=255, default="Nairobi")
    town = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    office_number = models.CharField(max_length=20)
    fax = models.CharField(max_length=30, )
    website_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.company_name
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        
class Departments(models.Model):
    company = models.CharField(max_length=255)
    department_name = models.CharField(max_length=255)
    number_of_employees = models.IntegerField()
    minimum_salary = models.DecimalField(max_digits=10, decimal_places=0)
    maximum_salary = models.DecimalField(max_digits=10, decimal_places=0)
    overtime_pay_perhour = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.department_name
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        
class Employee(models.Model):
    company = models.CharField(max_length=200)
    department =  models.CharField(max_length=180)
    employee = models.OneToOneField(User,related_name="employee", on_delete=models.CASCADE)
    email = models.EmailField(max_length=65, unique=True, verbose_name='email')
    username = models.CharField(max_length=40, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    mobile = models.CharField(max_length=15)
    address = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    employeeReg_Id = models.CharField(max_length=200)
    is_email_verified = models.BooleanField(default=False)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name 
    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
class Overtime(models.Model):
    my_employee = models.ForeignKey(Employee, on_delete=models.CASCADE)   
    overtime_date = models.DateField()
    overtime_hours = models.IntegerField()
    description = models.TextField()
    overtime_type = models.CharField(max_length=200)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=0)
    total = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.description  
    class Meta:
        verbose_name = "Over Time"
        verbose_name_plural = "Over Time"
    

    
    
    

    
    
