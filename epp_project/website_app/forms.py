from django.forms import ModelForm
from .models import Team

class TeamForm(ModelForm):
   class Meta:
      model = Team
      fields = [
         'team_name',
         'team_name_kana',
         'team_belong',
         'team_desc',
         'team_ninzu',
         'checkin_pretime_1',
         'checkin_koedashi',
         'duration_koed',
         'checkin_pretime_2',
         'duration_reha',
         'onstage_time',
         'duration_onst',
         'checkin_postime_1',
         'checkin_postime_2',
         'onstage_time_acc',
         'onstage_tien_acc',
         'team_rep_mail',
         'team_rep_tel',
         'team_equip',
         'file_artpic',
         'file_form',
         'file_stage',
         'team_rep',
         'note']

   def __init__(self, *args, **kwargs):
      view_type = kwargs.pop('view_type', None)
      super().__init__(*args, **kwargs)

      match view_type:
         case 'default':
            pass

         case 'initial':
            remove_fields = ['onstage_time_acc','onstage_tien_acc', 'checkin_postime_1', 'checkin_postime_2']
            for name in remove_fields:
               self.fields.pop(name, None)