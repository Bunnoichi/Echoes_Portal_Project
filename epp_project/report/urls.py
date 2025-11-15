from django.urls import path
from . import views

app_name = 'report'
urlpatterns = [
   path('report/report', views.report_reg, name='report_reg'),
   path('report/list', views.report_list, name='report_list'),
]