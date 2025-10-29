from django.forms import ModelForm
from .models import Team, Report

class TeamForm(ModelForm):
   class Meta:
      model = Team
      fields = ['team_name', 'team_desc', 'onstage_time', 'checkin_pretime_1', 'checkin_postime_1', 'checkin_charge_1', 'file_stage']

class ReportForm(ModelForm):
   class Meta:
      model = Report
      fields = ['repo_cont', 'repo_plac', 'repo_pter']