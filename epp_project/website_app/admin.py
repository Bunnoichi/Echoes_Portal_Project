from django.contrib import admin
from .models import Team

@admin.register(Team)
class PageAdmin(admin.ModelAdmin):
   readonly_fields = ['id', 'created_at', 'updated_at']