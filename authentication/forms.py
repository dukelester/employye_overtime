from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Enter a Valid Email address")
    class Meta:
        model = Account
        fields = ('email','username', 'password1','password2')
        
        def clean_email(self):
            email = self.cleaned_data['email'].lower()
            
            try:
                account = Account.objects.get(email=email)
            except Exception as e:
                return email
            
            raise forms.ValidationError("The email is already in use")
        def clean_username(self):
            username = self.cleaned_data['username']
            
            try:
                username = Account.objects.get(username=username)
            except Exception as e:
                return username
            
            raise forms.ValidationError("The username is already in use")

class AccountUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    
    class Meta:
        model = Account
        fields = ("full_name","email","phone","mobile","address","profile_image")

    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({'class' : 'form-control','placeholder':'Full name'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control','placeholder':'Email Address'})
        self.fields['phone'].widget.attrs.update({'class' : 'form-control','placeholder':'Phone Number'})
        self.fields['mobile'].widget.attrs.update({'class' : 'form-control','placeholder':'mobile name'})
        self.fields['address'].widget.attrs.update({'class' : 'form-control','placeholder':'address'})
        self.fields['profile_image'].widget.attrs.update({'class' : 'form-control','placeholder':'profile_image'})
        
       
        def clean_email(self):
            if self.is_valid():
                email = self.cleaned_data['email']
                try:
                    account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
                    
                except Account.DoesNotExist:
                    return email
                
                raise forms.ValidationError('The Email address "%s" is already in use' % email)
            
        def clean_full_name(self):
            if self.is_valid():
                full_name = self.cleaned_data['full_name']
                try:
                    account = Account.objects.exclude(pk=self.instance.pk).get(full_name=full_name)
                    
                except Account.DoesNotExist:
                    return full_name
                
                raise forms.ValidationError("Invalid Full name")
            
        def clean_phone(self):
            if self.is_valid():
                phone = self.cleaned_data['phone']
                try:
                    account = Account.objects.exclude(pk=self.instance.pk).get(phone=phone)
                    
                except Account.DoesNotExist:
                    return phone
                
                raise forms.ValidationError("The phone number is already taken")
            
        def clean_mobile(self):
            if self.is_valid():
                mobile = self.cleaned_data['mobile']
                try:
                    account = Account.objects.exclude(pk=self.instance.pk).get(mobile=mobile)
                    
                except Account.DoesNotExist:
                    return mobile
                
                raise forms.ValidationError("The mobile number is already taken")