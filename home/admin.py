from django.contrib import admin
from .models import Objective

# Register your models here.

class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']

admin.site.register(Objective, ObjectiveAdmin)
