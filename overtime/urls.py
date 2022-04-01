from django.urls import path
from .views import (homepageView,CalenderView,addDepartmentView,addDepartmentView,
                    addEmployeeView,companySettingsView )

urlpatterns = [
    path("",homepageView, name="homepage"),
    path("calendar", CalenderView, name="calendar"),
    path("company", addDepartmentView, name="company"),
    path('departments', addDepartmentView, name="departments"),
    path('employees',addEmployeeView, name="employees"),
    path('settings', companySettingsView, name="settings"),
    
    
]