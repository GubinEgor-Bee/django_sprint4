from .models import Post, Congratulation
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ("author",)
        widgets = {"pub_date": forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        )}


class CongratulationForm(forms.ModelForm):
    class Meta:
        model = Congratulation
        fields = ("text",)
