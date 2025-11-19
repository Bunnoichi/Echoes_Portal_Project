from django.urls import path
from . import views

app_name = 'website_app'
urlpatterns = [
   path('', views.index, name='index'),
   path('team/create/', views.team_initial_reg, name='team_initial_reg'),
   path('team/list/', views.team_list, name='team_list'),
   path('team/<uuid:id>/checkin', views.team_checkin, name='team_checkin'),
   path('team/<uuid:id>/detail', views.TeamDetailView.as_view(), name='team_detail'),
   path('team/<uuid:id>/detailpub', views.TeamPublicDetailView.as_view(), name='team_detail_pub'),
   path('team/<uuid:id>/update', views.team_update, name='team_update'),
]