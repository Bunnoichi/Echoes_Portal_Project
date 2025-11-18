from django.forms import ModelForm
from .models import Report

class ReportForm(ModelForm):
   class Meta:
      model = Report
      fields = ['repo_cont', 'repo_plac', 'repo_pter', 'repo_publicity']