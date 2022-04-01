from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_CEO = models.CharField(max_length=255)
    company_reg = models.CharField(max_length=255)
    no_of_staff = models.IntegerField()
    company_email = models.EmailField()
    description = models.TextField()
    address = models.TextField()
    postal_code = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    no_of_employees = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.company_name
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        
class Departments(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=255)
    number_of_employees = models.IntegerField()
    minimum_salary = models.DecimalField(max_digits=10, decimal_places=0)
    maximum_salary = models.DecimalField(max_digits=10, decimal_places=0)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.department_name
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        
class Employee(models.Model):
    department_name = models.ForeignKey(Departments, on_delete=models.CASCADE)
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    

    
    
    

    
    
