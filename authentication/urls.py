
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import (google_login, signup, login_function, logout_view, loginpage,verify_otp,
                    signuppage, ProfileView, UpdateProfile,password_reset_request,
                     activate_user)
urlpatterns = [
    path('login', login_function, name='login'),
    path('logout', logout_view, name='logout'),
    path('register', signup, name='register'),
    path('verify/',verify_otp, name='verify_phone'),
#     path('loginpage/', loginpage, name='loginpage'),
#     path('register.html', signuppage, name='signuppage'),
    path('activate-user/<uidb64>/<token>', activate_user, name='activate'),
    path('google_login', google_login, name='google_login'),
    path('profile/<int:user_id>/', ProfileView, name='profile'),
    path('<int:user_id>/update/', UpdateProfile, name='profile_update'),
    # path('search/', AccountSearchView, name='user_search'),
    path("password_reset", password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),      
    
]
