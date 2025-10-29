from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, LoginForm
from .models import CustomUser
from django.contrib import messages

class SignUpView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        # ?next= がURLについている場合、ログイン必須ページから来たとみなす
        if 'next' in request.GET:
            messages.info(request, 'このページを表示するにはログインが必要です。')
        return super().get(request, *args, **kwargs)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('website_app:index')
