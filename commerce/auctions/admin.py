from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Listing

class CustomUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('listings',)

# Register your models here.

admin.site.register(User, CustomUserAdmin)
admin.site.register(Listing)
