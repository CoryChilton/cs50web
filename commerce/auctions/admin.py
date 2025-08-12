from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Listing, Bid, Comment

class CustomUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('listings',)

# Register your models here.

admin.site.register(User, CustomUserAdmin)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)

