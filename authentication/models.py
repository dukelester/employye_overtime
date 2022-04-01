from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,phone,password=None, **kwargs):
        if username is None:
            raise TypeError("The user must have a Username!")
        if email is None:
            raise TypeError("The user must have a valid Email!")

        user = self.model(username=username, email=email,
            phone = phone)
        user.phone = phone
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self,email,username,password, phone):
        if username is None:
            raise TypeError("The user must have a Username!")
        if email is None:
            raise TypeError("The user must have a valid Email!")
        
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            phone = phone
            
        )
        user.phone = phone
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

def profile_image_filepath(self, filename):  # upload the image to
    return f'profile_images/{self.pk}/{"profile_image.png"}'


def get_default_profile_image():  # the default image
    return "user-04.jpg"


class UserProfile(models.Model):
    name = models.CharField(max_length=300)


class Account(AbstractBaseUser):
    USERS = (
        ('Hr', 'Hr'),
        ('Employee', 'Employee'),
    )
    email = models.EmailField(max_length=65, unique=True, verbose_name='email')
    username = models.CharField(max_length=40, unique=True)
    full_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15, unique=True)
    mobile = models.CharField(max_length=15)
    address = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_hr = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    user_type = models.CharField(max_length=34, choices=USERS)

    profile_image = models.ImageField(max_length=255, upload_to=profile_image_filepath,
                                      null=True, blank=True, default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)

    objects = MyAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  ['username','phone']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).
                                       index(f'profile_images/{self.pk}/'):]

    def has_module_perms(self, app_label):
        return True
