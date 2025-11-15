from django.forms import ModelForm
from .models import Team

class TeamForm(ModelForm):
   class Meta:
      model = Team
      fields = ['team_name', 'team_name_kana', 'team_desc', 'team_ninzu', 'team_rep', 'team_rep_mail', 'team_rep_tel', 'checkin_pretime_1', 'checkin_postime_1', 'checkin_pretime_2', 'checkin_postime_2', 'duration_reha', 'duration_onst', 'onstage_time', 'onstage_time_acc', 'file_form', 'file_stage', 'team_equip', 'note']

   def __init__(self, *args, **kwargs):
      view_type = kwargs.pop('view_type', None)
      super().__init__(*args, **kwargs)

      match view_type:
         case 'default':
            pass

         case 'initial':
            remove_fields = ['onstage_time_acc', 'checkin_postime_1', 'checkin_postime_2']
            for name in remove_fields:
               self.fields.pop(name, None)