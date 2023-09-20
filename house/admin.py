from django.contrib import admin
from .models import House


class HouseAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created']


admin.site.register(House, HouseAdmin)
