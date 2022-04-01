from django.urls import path
from .views import homepageView,CalenderView

urlpatterns = [
    path("",homepageView, name="homepage"),
    path("calendar", CalenderView, name="calendar"),
    
]