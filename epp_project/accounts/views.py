from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, LoginForm
from .models import CustomUser

class SignUpView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')
