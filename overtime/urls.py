from django.urls import path
from .views import homepageView

urlpatterns = [
    path("",homepageView, name="homepage"),
    
]