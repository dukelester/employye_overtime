# Create your views here.
from __future__ import print_function
from .forms import AccountUpdateForm
import requests
from datetime import datetime
import base64
import threading
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import Account
from . utils import generate_token
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = "Hey! Please Activate Your Account!"
    email_body = render_to_string('activate.html', {
        'user': user,
        'domain': current_site,
        'uid':  urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)})

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER, to=[user.email])
    email.send()
    # EmailThread(email).start()


def loginpage(request):
    return render(request, 'login.html')

def afterRegister(request):
    return render (request, 'coming-soon.html')

def signuppage(request):
    return render(request, 'register.html')
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"

def signup(request):
    
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('homepage')
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email', False)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        user_type = request.POST.get('user_type')

        print(username, email, password1, password2,
              phone, user_type)

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email exists!')
                return render(request, 'register.html', context)
            phone_exist =  User.objects.filter(phone=phone).exists()
            print(phone_exist, 'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
            if phone_exist:
                messages.add_message(request, messages.ERROR, "The phone Number is already in use!")
                return render(request, 'register.html', context)
            username_exist =  User.objects.filter(username=username).exists()
            print(username_exist, 'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
            if username_exist:
                messages.add_message(request, messages.ERROR, "The Username is already in use!")
                return render(request, 'register.html', context)
            if len(password1) < 6:
                messages.add_message(request, messages.ERROR, "Password Too Short!")
                return render(request, 'register.html', context)
            else:

                user = User.objects.create_user(email=email, username=email, password=password1,
                                                phone=phone
                                                )
                user.is_active = True
                user.phone = phone
                user.user_type = user_type
                
                # landlord = LandlordDetails(
                #     landlord=user,
                #     email=email, username=email,
                #     first_name=first_name,
                #     last_name=last_name,
                #     phone=phone,
                    
                # )
                # landlord.save()
                if user_type == 'Hr':
                    user.is_hr = True
                    # user.is_phone_verified = True
                    user.save()
                    messages.success(
                        request, 'HR Account created successfully!')
                    user = authenticate(username=email, password=password1)
                    send_activation_email(user, request)
                    
                    login(request, user)
                    user.save()
                    user.refresh_from_db()
                    # sending the activation link
                    return redirect('afterRegister')

                else:
                    user.is_hr = False
                   
                    messages.success(
                        request, 'Employee Account created successfully!')
                    user = authenticate(username=email, password=password1)
                    login(request, user)
                    
                    send_activation_email(user, request)
                   
                    user.save()
                    user.refresh_from_db()
                    print("sign up successful")
                    return redirect('afterRegister')
                   
        else:
            messages.info(request, 'Passwords do not match!')
            return render(request, 'register.html', context)
    else:
        return render(request, 'register.html')
def activate_user(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.add_message(
            request, messages.SUCCESS, "Your Account has been Verified successfully!")
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(reverse('login'))

    return render(request, 'activate_failed.html', {"user": user})

def login_function(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.user.is_authenticated:
        messages.add_message(
            request, messages.SUCCESS, "You Already Have An Account!")
        return redirect('homepage')
    else:
        if request.method == 'POST':
            username = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            print(username, password)
            user_exist = User.objects.filter(username=username).exists()
            print('ertyuiop[yuiop', user_exist, user.password)
            
            if user_exist:
                # return redirect('home')
            # email Verification
                if not user.is_email_verified:
                    messages.add_message(request, messages.ERROR,
                                        "Email Is not Verified. Please Check your Mail Box or the Spam Folder.")
                    return render(request, 'login.html', {})
                else:
                    
                    login(request, user)
                    
                if user is not None and user.is_active:
                    if user.is_active:
                        login(request, user,
                            backend='django.contrib.auth.backends.ModelBackend')
                        return redirect('homepage')
                    else:
                        messages.add_message(
                    request, messages.ERROR, "Your Account Is Innactive!")
                        return render(request, 'login.html')
                else:
                    messages.add_message(request, messages.ERROR, 'Wrong username/Password!')
                return render(request, 'login.html')
    return render(request, 'login.html', {})
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def ProfileView(request, *args, **kwargs):
    pass

#     context = {}

#     user_id = kwargs.get('user_id')
#     try:
#         account = Account.objects.get(pk=user_id)
#     except Account.DoesNotExist:
#         messages.add_message(
#             request, messages.ERROR, "You Do not Have An Account!")
#         return HttpResponse("The Account Does not exist!")
#     if account:
#         context['id'] = account.id
#         context['username'] = account.username
#         context['email'] = account.email
#         context['profile_image'] = account.profile_image.url
#         context['hide_email'] = account.hide_email
#         context['full_name'] = account.full_name
#         context['first_name'] = account.first_name
#         context['last_name'] = account.last_name
#         context['phone'] = account.phone
#         context['phone'] = account.phone
#         context['address'] = account.address
        
#         is_self = True
#         is_admin = False
#         is_superuser = False
#         is_staff = False
#         is_owner = True

#         user = request.user

#         if user.is_authenticated and user != account:
#             is_self = False
#             is_admin = False
#             is_superuser = False
#             is_staff = False
#             is_owner = False
#         elif not user.is_authenticated:
#             is_self = False
#             is_admin = False
#             is_superuser = False
#             is_staff = False
#             # is_owner = False

#         context['is_self'] = is_self
#         context['is_admin'] = is_admin
#         context['is_superuser'] = is_superuser
#         context['is_staff'] = is_staff
#         context['is_owner'] = is_owner
#         context['BASE_URL'] = settings.BASE_URL
#         if request.user.is_landlord:
#             context['is_landlord'] = account.is_landlord

#         tenant = TenantDetails.objects.filter(tenant=request.user)
#         if tenant:
            
            
            
#             context['tenant'] = tenant
#             context['house_number'] = tenant[0].house_number
#             context['overpayment'] = tenant[0].overpayment
#             context['arrears'] = tenant[0].arrears
#             context['date_allocated'] = tenant[0].date_allocated
#             context['rent_due_date'] = tenant[0].rent_due_date
            
        
#             messages.add_message(request,messages.INFO, "Your Water Bill will be Updates Soon!")
#             return render(request, 'profile.html', context)
                

       
#             print(tenant[0].house_number, 'wertyuiopppppppppppppppppppppp',WaterBills.objects.latest('created_at') )

#     return render(request, 'profile.html', context)


@login_required(login_url='login')
def UpdateProfile(request, *args, **kwargs):
    pass
    # user_id = kwargs.get('user_id')
    # if not request.user.is_authenticated:
    #     return redirect('login')

    # if request.method == 'POST':
    #     form = AccountUpdateForm(request.POST,request.FILES, instance=request.user)
    #     if form.is_valid():
    #         form.save()

    #     else:
    #         form = AccountUpdateForm(
    #             initial={
    #                 "email": request.user.email,
    #                 "full_name": request.user.full_name,
    #                 "full_name": request.user.full_name,
    #             }
    #         )
    #     context = {}
    #     context['user_update_form'] = form
    #     messages.add_message(
    #         request, messages.SUCCESS, "Your Profile has been Updated Successfully!")
    #     print("profile update complete")

    # return render(request, 'profile.html', context)



def password_reset_request(request): 
    current_site = get_current_site(request)
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':current_site, 
                    'site_name': 'EMp',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http', #https
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'AWS_verified_email_address', [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')
                        
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect ('login')
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/forgot-password.html", context={"password_reset_form":password_reset_form})
