from django import forms
from .models import Post, Comment, Profile
from django.core.exceptions import ValidationError
from django.utils import timezone


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'pub_date', 'location', 'category', 'image']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pub_date = cleaned_data.get('pub_date')
        if pub_date and pub_date > timezone.now():
            if not self.instance.pk and not self.initial.get('author'):
                raise ValidationError(
                    "Отложенные публикации доступны только для "
                    "авторизованных пользователей")
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text and len(text.strip()) < 3:
            raise ValidationError(
                "Комментарий должен содержать хотя бы 3 символа")
        return text


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['bio', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if hasattr(profile, 'user'):
            user = profile.user
            user.first_name = self.cleaned_data.get('first_name', '')
            user.last_name = self.cleaned_data.get('last_name', '')
            user.email = self.cleaned_data.get('email', '')
            if commit:
                user.save()
                profile.save()
        return profile
