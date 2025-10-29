from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from datetime import datetime
from .forms import TeamForm, ReportForm
from .models import Team, Report
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(View):
   def get(self, request):
         datetime_now = datetime.now()
         return render(request, 'echoes/index.html',
                       {'datetime_now': datetime_now})
   
class TeamCreateView(LoginRequiredMixin, View):
  login_url = 'accounts:login'
  redirect_field_name = 'next'
  def get(self, request):
      form = TeamForm()
      return render(request, 'echoes/team_initial_reg.html', {'form': form})

  def post(self, request):
      form = TeamForm(request.POST, request.FILES)
      if form.is_valid():
        form.save()
        return redirect('website_app:index')
      return render(request, 'echoes/team_initial_reg.html', {'form': form})
      
class TeamListView(View):
    def get(self, request):
        team_list = Team.objects.order_by('onstage_time')
        return render(request, 'echoes/team_list.html', {'team_list': team_list})

class TeamCheckinView(LoginRequiredMixin, View):
  login_url = 'accounts:login'
  redirect_field_name = 'next'
  def get(self, request, id):
      form = TeamForm(instance=get_object_or_404(Team, id=id))
      return render(request, 'echoes/team_checkin.html', {'form': form})
  
  def post(self, request, id):
      form = TeamForm(request.POST, instance=get_object_or_404(Team, id=id))
      if form.is_valid():
        form.save()
        return redirect('website_app:team_list')
      return render(request, 'echoes/team_checkin.html', {'form': form})
      
class TeamDetailView(LoginRequiredMixin, View):
  login_url = 'accounts:login'
  redirect_field_name = 'next'
  def get(self, request, id):
    team = get_object_or_404(Team, id=id)
    return render(request, 'echoes/team_detail.html', {'team': team})
  
class ReportCreateView(View):
    def get(self, request):
        form = ReportForm()
        return render(request, 'echoes/report_reg.html', {'form': form})
    
    def post(self, request):
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
          form.save()
          return redirect('website_app:index')
        return render(request, 'echoes/report_reg.html', {'form': form})
    
class ReportListView(LoginRequiredMixin, View):
  login_url = 'accounts:login'
  redirect_field_name = 'next'
  def get(self, request):
      report_list = Report.objects.order_by('created_at')
      return render(request, 'echoes/report_list.html', {'report_list': report_list})

index = IndexView.as_view()
team_initial_reg = TeamCreateView.as_view()
team_list = TeamListView.as_view()
team_checkin = TeamCheckinView.as_view()
team_detail = TeamDetailView.as_view()
report_reg = ReportCreateView.as_view()
report_list = ReportListView.as_view()