from django.contrib import admin
from .models import Report

@admin.register(Report)
class PageAdmin(admin.ModelAdmin):
   readonly_fields = ['id', 'created_at']