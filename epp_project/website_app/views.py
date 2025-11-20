from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import TeamForm
from .models import Team
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from datetime import timedelta
from django.views.generic import DetailView
from report.models import Report
from datetime import datetime


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



    if (onstage_now is None):
       onstage_now = onstage_pos
    if (onstage_pos is None):
       onstage_pos = onstage_now

    if (onstage_now is None and onstage_pos is None):
       onstage_pos = empty_team()
       onstage_now = empty_team()
       

    # リハ + 本番 合計分数
    total_minutes = onstage_now.duration_reha + onstage_now.duration_onst
    total_seconds = total_minutes * 60

    start_reha = onstage_now.onstage_time - timedelta(minutes=onstage_now.duration_reha)
    end_stage = onstage_now.onstage_time + timedelta(minutes=onstage_now.duration_onst)

    # 0〜100%の範囲に収める
    progress = max(0, min(100, ((timezone_now - start_reha).total_seconds() / total_seconds) * 100))

    progress_team = onstage_now



    if progress == 100:
        progress_team = onstage_pos
        
        total_minutes = onstage_pos.duration_reha + onstage_pos.duration_onst
        total_seconds = total_minutes * 60
        start_reha = onstage_pos.onstage_time - timedelta(minutes=onstage_pos.duration_reha)
        end_stage = onstage_pos.onstage_time + timedelta(minutes=onstage_pos.duration_onst)

        # 0〜100%の範囲に収める
        progress = max(0, min(100, ((timezone_now - start_reha).total_seconds() / total_seconds) * 100))



    if (end_stage - timezone_now).total_seconds() > 180:
        bar_class = "bg-success"
    elif (end_stage - timezone_now).total_seconds() < 60:
        bar_class = "bg-danger"
    elif (end_stage - timezone_now).total_seconds() < 180:
        bar_class = "bg-warning"

    if ( start_reha < timezone_now and timezone_now < progress_team.onstage_time):
        now_status = {'st':'リハ中', 'co': 'bg-warning'}
    elif (progress_team.onstage_time < timezone_now and timezone_now < end_stage):
        now_status = {'st':'本番中', 'co': 'bg-danger'}
    else:
        now_status = {'st':'待機中', 'co': 'bg-transparent'}


    
    progress_info = {
       'progress': progress,
       'now_status': now_status,
       'bar_class': bar_class,
       'start_reha': start_reha,
       'total_minutes': total_minutes,
       'end': end_stage,
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
        'now': timezone_now,
        'report': report,
        'team_list': Team.objects.order_by('onstage_time'),
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
      team_name = get_object_or_404(Team, id=id).team_name
      form = TeamForm(instance=get_object_or_404(Team, id=id), view_type='default')
      return render(request, 'echoes/team_checkin.html', {'form': form, 'wanted_field':wanted_field, 'team_name': team_name})
  
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
  
class TeamUpdateView(PermissionRequiredMixin, LoginRequiredMixin, View):
  login_url = 'accounts:login'
  redirect_field_name = 'next'
  permission_required = 'website_app.update_information'
  
  def get(self, request, id):
      team_name = get_object_or_404(Team, id=id).team_name
      form = TeamForm(instance=get_object_or_404(Team, id=id), view_type='default')
      return render(request, 'echoes/team_update.html', {'form': form, 'team_name': team_name})

  def post(self, request, id):
      form = TeamForm(request.POST, request.FILES, instance=get_object_or_404(Team, id=id))
      if form.is_valid():
        form.save()
        return redirect('website_app:team_list')
      return render(request, 'echoes/team_update.html', {'form': form})

class TeamPublicDetailView(DetailView):
    model = Team
    template_name = 'echoes/team_detail_pub.html'
    context_object_name = 'team'
    pk_url_kwarg = 'id'  # URLのパラメータ名が pk でない場合に指定

    EXCLUDE_FIELDS = [
        'team_ninzu',
        'checkin_postime_1',
        'checkin_postime_2',
        'onstage_time_acc',
        'onstage_tien_acc',
        'team_rep',
        'team_rep_mail',
        'team_rep_tel',
        'team_equip',
        'file_form',
        'file_stage',
        'note']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        team = context.pop("team")  # ★ 完全に削除（テンプレートに渡らない）

        public_data = {}
        for field in team._meta.get_fields():
            if field.name not in self.EXCLUDE_FIELDS:
                public_data[field.name] = getattr(team, field.name)

        context["team"] = public_data  # team を public_data に差し替える

        return context

index = IndexView.as_view()
team_initial_reg = TeamCreateView.as_view()
team_list = TeamListView.as_view()
team_update = TeamUpdateView.as_view()
team_checkin = TeamCheckinView.as_view()
team_detail = TeamDetailView.as_view()
team_detail_pub = TeamPublicDetailView.as_view()


def custom_permission_denied_view(request, exception=None):
    response = render(request, "403.html")
    response.status_code = 403
    return response

DEFAULT_DATETIME = timezone.make_aware(datetime(2025, 12, 31, 0, 0))

def empty_team():
    return Team(
        team_name="終了",
        onstage_time=DEFAULT_DATETIME,
        checkin_pretime_1=DEFAULT_DATETIME,
        checkin_pretime_2=DEFAULT_DATETIME,
    )