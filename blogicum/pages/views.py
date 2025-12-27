from django.views.generic import TemplateView
from django.shortcuts import render


class AboutTemplateView(TemplateView):
    """Информация о проекте."""

    template_name = "pages/about.html"


class RulesTemplateView(TemplateView):
    """Правила проекта."""

    template_name = "pages/rules.html"


def page_not_found(request, exception):
    """Обработчик ошибки 404."""
    return render(request, "pages/404.html", status=404)


def csrf_failure(request, reason=""):
    """Обработчик ошибки 403."""
    return render(request, "pages/403csrf.html", status=403)


def error_on_the_server(request, exception=None):
    """Обработчик ошибки 500."""
    return render(request, "pages/500.html", status=500)
