from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateInput, ClearableFileInput
from django.forms import FileInput
from .models import Comment, Profile, Content, SimilarityVote


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите ваш комментарий'}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Ваш никнейм может состоять только из цифр, букв и следующих символов: @/./+/-/_</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Ваш пароль не должен быть схожим с другой персональной информацией.</li><li>Ваш пароль должен состоять минимум из 8 символов.</li><li>Ваш пароль не должен быть очевидным.</li><li>Ваш пароль не должен состоять только из цифр.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Подтвердите пароль введенный выше.</small></span>'

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(label='Дата рождения', widget=DateInput(attrs={'type': 'date'}))

    avatar = forms.ImageField(
        label='Аватар',
        widget=ClearableFileInput(attrs={'multiple': False}),
        required=False,
    )
    class Meta:
        model = Profile
        fields = ['name', 'date_of_birth', 'gender', 'location', 'contact_info', 'interests', 'skills', 'about_me', 'avatar', 'status']
        labels = {
            'name': 'Имя',
            'gender': 'Пол',
            'location': 'Местоположение',
            'contact_info': 'Контактная информация',
            'interests': 'Интересы',
            'skills': 'Навыки',
            'about_me': 'О себе',
            'status': 'Статус',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['date_of_birth'].widget.attrs['type'] = 'date'


class SimilarContentForm(forms.Form):
    similar_content = forms.ModelChoiceField(queryset=Content.objects.all(), label='Похожее произведение')

class SimilarityVoteForm(forms.ModelForm):
    class Meta:
        model = SimilarityVote
        fields = ['vote']
