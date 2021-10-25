from django import forms
from django.forms import ModelForm
from spodaily_api.models import User, Session, Activity
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EditUserForm(ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'name', 'birth', 'height', 'weight', 'sexe']


class AddSessionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddSessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = ['name', 'date']


class AddActivityForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddActivityForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Activity
        fields = ['exercise_id', 'sets', 'repetition', 'rest', 'weight']