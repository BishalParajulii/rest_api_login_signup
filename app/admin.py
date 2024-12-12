# admin.py
from django.contrib import admin
from .models import User, Organization

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'phone_number', 'blood_group', 'district', 'province']
    search_fields = ['email', 'name']

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'district', 'province']
    search_fields = ['email', 'name']

admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
