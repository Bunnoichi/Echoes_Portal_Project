from django.shortcuts import render
from django.views import View
from website_app.models import Team
from django.utils import timezone
from datetime import timedelta
from report.models import Report
from datetime import datetime

class IndexView(View):
    def get(self, request):
        timezone_now = timezone.now()


        onstage_now = first_or_empty(
            Team.objects.filter(onstage_time__lt=timezone_now)
            .order_by('-onstage_time')
        )

        onstage_pos = first_or_empty(
            Team.objects.filter(onstage_time__gte=timezone_now)
            .order_by('onstage_time')
        )

        onstage_pos2 = nth_or_empty(
            Team.objects.filter(onstage_time__gte=timezone_now)
            .order_by('onstage_time'),
            1
        )

        # checkin1_now = first_or_empty(
        #     Team.objects.filter(checkin_pretime_1__lt=timezone_now)
        #     .order_by('-checkin_pretime_1')
        # )

        # checkin1_pos = first_or_empty(
        #     Team.objects.filter(checkin_pretime_1__gte=timezone_now)
        #     .order_by('checkin_pretime_1')
        # )

        # checkin1_pos2 = nth_or_empty(
        #     Team.objects.filter(checkin_pretime_1__gte=timezone_now)
        #     .order_by('checkin_pretime_1'),
        #     1
        # )

        # checkin2_now = first_or_empty(
        #     Team.objects.filter(checkin_pretime_2__lt=timezone_now)
        #     .order_by('-checkin_pretime_2')
        # )

        # checkin2_pos = first_or_empty(
        #     Team.objects.filter(checkin_pretime_2__gte=timezone_now)
        #     .order_by('checkin_pretime_2')
        # )

        # checkin2_pos2 = nth_or_empty(
        #     Team.objects.filter(checkin_pretime_2__gte=timezone_now)
        #     .order_by('checkin_pretime_2'),
        #     1
        # )

        if (onstage_now is None):
            onstage_now = onstage_pos
        if (onstage_pos is None):
            onstage_pos = onstage_now

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
            'onstage_pos': onstage_pos,
            'onstage_pos2': onstage_pos2,
            # 'checkin1_now': checkin1_now,
            # 'checkin1_pos': checkin1_pos,
            # 'checkin1_pos2': checkin1_pos2,
            # 'checkin2_now': checkin2_now,
            # 'checkin2_pos': checkin2_pos,
            # 'checkin2_pos2': checkin2_pos2,
            'now': timezone_now,
            'report': report,
        }
        
        return render(request, 'status/status.html', context)

index = IndexView.as_view()

DEFAULT_DATETIME = timezone.make_aware(datetime(2025, 12, 31, 0, 0))

def empty_team():
    return Team(
        team_name="終了",
        onstage_time=DEFAULT_DATETIME,
        checkin_pretime_1=DEFAULT_DATETIME,
        checkin_pretime_2=DEFAULT_DATETIME,
    )

def first_or_empty(qs):
    obj = qs.first()
    return obj if obj is not None else empty_team()

def nth_or_empty(qs, n):
    try:
        return qs[n]
    except IndexError:
        return empty_team()