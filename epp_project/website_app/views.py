from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import TeamForm
from .models import Team
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from datetime import timedelta
from django.views.generic import DetailView
from report.models import Report

class IndexView(View):
  def get(self, request):
    timezone_now = timezone.now()

    # --- ORMを使ってデータ取得 ---
    # 現在より前のイベント（過去）を時刻が近い順に1件取得
    onstage_now = (
        Team.objects.filter(onstage_time__lt=timezone_now)  # 現在より前
        .order_by('-onstage_time')                  # 時刻が近いもの（降順）
        .first()                                    # 最初の1件だけ
    )
    # 現在より後のイベント（未来）を時刻が近い順に1件取得
    onstage_pos = (
        Team.objects.filter(onstage_time__gte=timezone_now) # 現在以降
        .order_by('onstage_time')                   # 時刻が近いもの（昇順）
        .first()
    )
    onstage_pos2 = (
        Team.objects.filter(onstage_time__gte=timezone_now)
        .order_by('onstage_time')[1]
    )

    checkin1_now = (
        Team.objects.filter(checkin_pretime_1__lt=timezone_now)
        .order_by('-checkin_pretime_1')
        .first()
    )
    checkin1_pos = (
        Team.objects.filter(checkin_pretime_1__gte=timezone_now)
        .order_by('checkin_pretime_1')
        .first()
    )
    checkin1_pos2 = (
        Team.objects.filter(checkin_pretime_1__gte=timezone_now)
        .order_by('checkin_pretime_1')[1]
    )

    checkin2_now = (
        Team.objects.filter(checkin_pretime_2__lt=timezone_now)
        .order_by('-checkin_pretime_2')
        .first()
    )
    checkin2_pos = (
        Team.objects.filter(checkin_pretime_2__gte=timezone_now)
        .order_by('checkin_pretime_2')
        .first()
    )
    checkin2_pos2 = (
        Team.objects.filter(checkin_pretime_2__gte=timezone_now)
        .order_by('checkin_pretime_2')[1]
    )

    # リハ + 本番 合計分数
    total_minutes = onstage_now.duration_reha + onstage_now.duration_onst

    total_seconds = total_minutes * 60
    elapsed = onstage_now.onstage_time - timedelta(minutes=onstage_now.duration_reha)
    end = onstage_now.onstage_time + timedelta(minutes=onstage_now.duration_onst)

    # 0〜100%の範囲に収める
    progress = max(0, min(100, ((timezone_now - elapsed).total_seconds() / total_seconds) * 100))

    progress_team = onstage_now

    next_reha = onstage_pos.onstage_time - timedelta(minutes=onstage_now.duration_reha)

    if (end - timezone_now).total_seconds() > 180:
        bar_class = "bg-success"
    elif (end - timezone_now).total_seconds() < 60:
        bar_class = "bg-danger"
    elif (end - timezone_now).total_seconds() < 180:
        bar_class = "bg-warning"

    if progress == 100 and next_reha < timezone_now:
        progress_team = onstage_pos
        bar_class = "bg-primary"
        
        total_minutes = onstage_pos.duration_reha + onstage_pos.duration_onst
        total_seconds = total_minutes * 60
        elapsed = onstage_pos.onstage_time - timedelta(minutes=onstage_pos.duration_reha)
        end = onstage_pos.onstage_time + timedelta(minutes=onstage_pos.duration_onst)

        # 0〜100%の範囲に収める
        progress = max(0, min(100, ((timezone_now - elapsed).total_seconds() / total_seconds) * 100))
    
    progress_info = {
       'progress': progress,
       'bar_class': bar_class,
       'start_reha': elapsed,
       'total_minutes': total_minutes,
       'end': end,
       'progress_team': progress_team,
    }


    report = {
       'repo_tweet' : Report.objects.filter(repo_tweet=True).order_by('created_at').last(),
       'repo_staff' : Report.objects.filter(repo_tweet=False, repo_publicity='only_staff').order_by('created_at').last(),
       'repo_public' : Report.objects.filter(repo_tweet=False, repo_publicity='public').order_by('created_at').last(),
    }

    context = {
        'progress_info':progress_info,
        'onstage_now': onstage_now,
        'onstage_pos': onstage_pos,
        'onstage_pos2': onstage_pos2,
        'checkin1_now': checkin1_now,
        'checkin1_pos': checkin1_pos,
        'checkin1_pos2': checkin1_pos2,
        'checkin2_now': checkin2_now,
        'checkin2_pos': checkin2_pos,
        'checkin2_pos2': checkin2_pos2,
        'now': timezone_now,
        'report': report,
    }
    
    return render(request, 'echoes/index.html', context)

class TeamCreateView(PermissionRequiredMixin, LoginRequiredMixin, View):
  login_url = 'accounts:login'
  redirect_field_name = 'next'
  permission_required = 'initial_registration'

  def get(self, request):
      form = TeamForm(view_type='initial')
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

class TeamCheckinView(PermissionRequiredMixin, LoginRequiredMixin, View):
  login_url = 'accounts:login'
  redirect_field_name = 'next'
  permission_required = 'checkin'

  def get(self, request, id):
      wanted_field = ['onstage_time_acc', 'onstage_tien_acc', 'checkin_postime_1', 'checkin_postime_2']
      form = TeamForm(instance=get_object_or_404(Team, id=id), view_type='default')
      return render(request, 'echoes/team_checkin.html', {'form': form, 'wanted_field':wanted_field})
  
  def post(self, request, id):
      form = TeamForm(request.POST, instance=get_object_or_404(Team, id=id))
      if form.is_valid():
        form.save()
        return redirect('website_app:team_list')
      return render(request, 'echoes/team_checkin.html', {'form': form})
      
class TeamDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'echoes/team_detail.html'
    context_object_name = 'team'
    pk_url_kwarg = 'id'  # URLのパラメータ名が pk でない場合に指定
    login_url = 'accounts:login'
    permission_required = 'website_app.view_detail'
  
class TeamUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
  login_url = 'accounts:login'
  redirect_field_name = 'next'
  permission_required = 'website_app.update_information'
  
  def get(self, request, id):
      form = TeamForm(instance=get_object_or_404(Team, id=id), view_type='default')
      return render(request, 'echoes/team_update.html', {'form': form})

  def post(self, request, id):
      form = TeamForm(request.POST, request.FILES, instance=get_object_or_404(Team, id=id))
      if form.is_valid():
        form.save()
        return redirect('website_app:team_list')
      return render(request, 'echoes/team_update.html', {'form': form})

index = IndexView.as_view()
team_initial_reg = TeamCreateView.as_view()
team_list = TeamListView.as_view()
team_update = TeamUpdateView.as_view()
team_checkin = TeamCheckinView.as_view()
team_detail = TeamDetailView.as_view()