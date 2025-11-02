from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import TeamForm, ReportForm
from .models import Team, Report
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

class IndexView(View):
  def get(self, request):
    timezone_now = timezone.now()

    # --- ORMを使ってデータ取得 ---
    # 現在より前のイベント（過去）を時刻が近い順に1件取得
    previous_event = (
        Team.objects.filter(onstage_time__lt=timezone_now)  # 現在より前
        .order_by('-onstage_time')                  # 時刻が近いもの（降順）
        .first()                                    # 最初の1件だけ
    )
    # 現在より後のイベント（未来）を時刻が近い順に1件取得
    next_event = (
        Team.objects.filter(onstage_time__gte=timezone_now) # 現在以降
        .order_by('onstage_time')                   # 時刻が近いもの（昇順）
        .first()
    )

    context = {
        'previous_event': previous_event,
        'next_event': next_event,
        'now': timezone_now,
    }
    
    return render(request, 'echoes/index.html', context)
   
class TeamCreateView(LoginRequiredMixin, View):
  login_url = 'accounts:login'
  redirect_field_name = 'next'
  def get(self, request):
      form = TeamForm(initial_field=True)
      return render(request, 'echoes/team_initial_reg.html', {'form': form})

  def post(self, request):
      form = TeamForm(request.POST, request.FILES,initial_field=True)
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
      form = TeamForm(instance=get_object_or_404(Team, id=id), initial_field=False)
      return render(request, 'echoes/team_checkin.html', {'form': form})
  
  def post(self, request, id):
      form = TeamForm(request.POST, instance=get_object_or_404(Team, id=id), initial_field=False)
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
  
class TeamUpdateView(LoginRequiredMixin, View):
  login_url = 'accounts:login'
  redirect_field_name = 'next'
  def get(self, request, id):
      form = TeamForm(instance=get_object_or_404(Team, id=id), initial_field=False)
      return render(request, 'echoes/team_update.html', {'form': form})

  def post(self, request, id):
      form = TeamForm(request.POST, request.FILES, instance=get_object_or_404(Team, id=id), initial_field=False)
      if form.is_valid():
        form.save()
        return redirect('website_app:team_list')
      return render(request, 'echoes/team_update.html', {'form': form})
  
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
team_update = TeamUpdateView.as_view()
team_checkin = TeamCheckinView.as_view()
team_detail = TeamDetailView.as_view()
report_reg = ReportCreateView.as_view()
report_list = ReportListView.as_view()