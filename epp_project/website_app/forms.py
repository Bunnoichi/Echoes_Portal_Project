from django.forms import ModelForm
from .models import Team, Report

class TeamForm(ModelForm):
   class Meta:
      model = Team
      fields = ['team_name', 'team_desc', 'onstage_time', 'onstage_time_acc',  'checkin_pretime_1', 'checkin_postime_1', 'checkin_charge_1','checkin_pretime_2', 'checkin_postime_2', 'checkin_charge_2', 'file_form', 'file_stage']

   def __init__(self, *args, **kwargs):
      view_type = kwargs.pop('view_type', None)
      super().__init__(*args, **kwargs)

      match view_type:
         case 'default':
            pass

         case 'initial':
            remove_fields = ['onstage_time_acc', 'checkin_postime_1', 'checkin_charge_1', 'checkin_postime_2', 'checkin_charge_2']
            for name in remove_fields:
               self.fields.pop(name, None)
         
class ReportForm(ModelForm):
   class Meta:
      model = Report
      fields = ['repo_cont', 'repo_plac', 'repo_pter']