from django import forms
from .models import Post, Comment, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'created_at')
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format=('%Y-%m-%d %H:%M'),
            ),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea({'cols': '22', 'rows': '5'}),
        }
