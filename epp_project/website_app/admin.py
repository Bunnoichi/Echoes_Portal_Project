from django.contrib import admin
from .models import Team, Report


@admin.register(Team)
class PageAdmin(admin.ModelAdmin):
   readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(Report)
class PageAdmin(admin.ModelAdmin):
   readonly_fields = ['id', 'created_at']