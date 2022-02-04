from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email']:
            self.fields[fieldname].help_text = None


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['name', 'address', 'bio', 'phone_number', 'image']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        for fieldname in ['name', 'address', 'bio', 'phone_number', 'image']:
            self.fields[fieldname].help_text = None


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = RoomModel
        fields = ['topic', 'name', 'description']


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'write your message here.....',
        'aria-describedby': 'button-addon1',
        'class': 'form-control'
    }))

    class Meta:
        model = MessageModel
        fields = ['body']


class CommentUpdateForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={
        'aria-describedby': 'button-addon2',
        'class': 'form-control'
    }))

    class Meta:
        model = MessageModel
        fields = ['body']


class TopicForm(forms.ModelForm):
    name = forms.CharField(label='Add Topic ', widget=forms.TextInput(attrs={
        'aria-describedby': 'button-addon3',
        'class': 'form-control'
    }))

    class Meta:
        model = TopicModel
        fields = ['name']
