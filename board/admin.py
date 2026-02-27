from django.contrib import admin

from .models import *


admin.site.register(CustomUser)
admin.site.register(Company)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)