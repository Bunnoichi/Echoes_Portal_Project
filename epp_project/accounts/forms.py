from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username')

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="メールアドレス")
