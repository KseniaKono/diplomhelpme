from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('commentator','text','content_id')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите ваш комментарий'}),
            'content_id': forms.HiddenInput(),
        }
