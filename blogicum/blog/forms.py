from .models import Post, Congratulation
from django import forms
from django.contrib.auth import get_user_model


class PostForm(forms.ModelForm):
    """Форма для создания и редактирования постов."""

    class Meta:
        """
        Конфигурация формы, связанная с моделью Post.
        Исключено поле 'author', так как автор определяется автоматически.
        """

        model = Post
        exclude = ("author",)
        widgets = {
            "pub_date": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }

        labels = {
            "title": "Заголовок",
            "text": "Текст поста",
            "pub_date": "Дата и время публикации",
            "author": "Автор публикации",
            "location": "Местоположение",
            "category": "Категория",
            "image": "Изображение",
            "is_published": "Опубликовано",
            "created_at": "Добавлено",
        }


class CongratulationForm(forms.ModelForm):
    """Форма для создания комментариев к постам."""

    class Meta:
        """Конфигурация формы, связанной с моделью Congratulation."""

        model = Congratulation
        fields = ("text",)
        labels = {
            "text": "Текст комментария",
        }
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "cols": 40,
                    "placeholder": "Оставьте свой комментарий здесь...",
                }
            )
        }


class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя."""

    class Meta:
        """Вложенный класс для конфигурации формы, связанной с моделью User."""

        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

        labels = {
            "username": "Имя пользователя",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Электронная почта",
        }
