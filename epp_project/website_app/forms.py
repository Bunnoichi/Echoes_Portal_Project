from django.forms import ModelForm
from .models import Team, Report

class TeamForm(ModelForm):
   class Meta:
      model = Team
      fields = ['team_name', 'team_desc', 'onstage_time', 'onstage_time_acc',  'checkin_pretime_1', 'checkin_postime_1', 'checkin_charge_1','checkin_pretime_2', 'checkin_postime_2', 'checkin_charge_2', 'file_form', 'file_stage']

   def __init__(self, *args, initial_field=True, **kwargs):
      super().__init__(*args, **kwargs)
      if initial_field:
         self.fields.pop('onstage_time_acc', None)
         self.fields.pop('checkin_postime_1', None)
         self.fields.pop('checkin_postime_2', None)

class ReportForm(ModelForm):
   class Meta:
      model = Report
      fields = ['repo_cont', 'repo_plac', 'repo_pter']