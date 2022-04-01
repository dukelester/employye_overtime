from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    list_display =('username', 'email', 'is_staff','is_superuser','is_admin', 'date_joined',
                   'last_login')
    search_fields = ('username', 'email',)
    readonly_fields = ('id', 'date_joined', 'last_login','user_type','is_hr')
    
    filter_fields = ()
    filter_horizontal = ()
    fieldsets = ()
    list_filter = ()
    

admin.site.register(Account, AccountAdmin)
