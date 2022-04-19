from django.urls import path
from .views import (homepageView,CalenderView,addDepartmentView,addDepartmentView,
                    addEmployeeView,companySettingsView ,addOverTimeView,requestForOvertime,approveNow)

urlpatterns = [
    path("",homepageView, name="homepage"),
    path("calendar", CalenderView, name="calendar"),
    path("company", addDepartmentView, name="company"),
    path('departments', addDepartmentView, name="departments"),
    path('employees',addEmployeeView, name="employees"),
    path('settings', companySettingsView, name="settings"),
    path('overtime',addOverTimeView, name="overTime"),
    path('request-overtime', requestForOvertime, name='request-overtime'),
    path('approve_now/<str:pk>', approveNow, name="approve_now"),
    
]