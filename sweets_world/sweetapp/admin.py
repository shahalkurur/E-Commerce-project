from django.contrib import admin
from .models import CustomUser,Profile
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(CustomUser,UserAdmin)
admin.site.register(Profile)


class CustomUserAdmin(UserAdmin):
    list_display = ( 'username','email', 'mobile', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    # Remove 'username' from the fieldsets
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'username','mobile',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Remove 'username' from the add_fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','date_joined','mobile','email', 'password1', 'password2'),
        }),
    )
    list_filter = ()
    
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
    

