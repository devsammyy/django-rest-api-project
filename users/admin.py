from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    read_only_field = ['id',]


admin.site.register(Profile)
