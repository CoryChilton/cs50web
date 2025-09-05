from django.contrib import admin
from .models import User, Post

class CustomUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('following',)

class CustomPostAdmin(admin.ModelAdmin):
    filter_horizontal = ('likers',)

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, CustomPostAdmin)