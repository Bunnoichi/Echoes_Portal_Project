from django.forms import ModelForm
from .models import Report

class ReportForm(ModelForm):
   class Meta:
      model = Report
      fields = ['repo_cont', 'repo_plac', 'repo_pter', 'repo_publicity', 'repo_tweet']

   def clean(self):
      cleaned_data = super().clean()
      use_default = cleaned_data.get("repo_tweet")

      if use_default:
         cleaned_data["repo_publicity"] = 'only_staff'  # デフォルト値を強制

      return cleaned_data
   
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['repo_publicity'].required = False