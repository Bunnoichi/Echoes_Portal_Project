from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import ReportForm
from .models import Report
from django.contrib.auth.mixins import LoginRequiredMixin
  
class ReportCreateView(View):
    def get(self, request):
        form = ReportForm()
        return render(request, 'echoes/report_reg.html', {'form': form})
    
    def post(self, request):
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
          form.save()
          return redirect('website_app:index')
        return render(request, 'echoes/report_reg.html', {'form': form})
    
class ReportListView(LoginRequiredMixin, View):
  login_url = 'accounts:login'
  redirect_field_name = 'next'
  def get(self, request):
      report_list = Report.objects.order_by('created_at')
      return render(request, 'echoes/report_list.html', {'report_list': report_list})

report_reg = ReportCreateView.as_view()
report_list = ReportListView.as_view()