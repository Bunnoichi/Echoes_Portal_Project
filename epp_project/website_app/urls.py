from django.urls import path
from . import views

app_name = 'website_app'
urlpatterns = [
   path('', views.index, name='index'),
   path('team/create/', views.team_initial_reg, name='team_initial_reg'),
   path('team/list/', views.team_list, name='team_list'),
   path('team/<uuid:id>/checkin', views.team_checkin, name='team_checkin'),
   path('team/<uuid:id>/detail', views.team_detail, name='team_detail'),
   path('report/report', views.report_reg, name='report_reg'),
   path('report/list', views.report_list, name='report_list'),
]