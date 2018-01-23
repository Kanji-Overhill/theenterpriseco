from django.contrib import admin
from .models import Manager, SuperAdmin

admin.site.register(Manager)
admin.site.register(SuperAdmin)