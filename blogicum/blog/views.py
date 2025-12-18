from django.shortcuts import get_object_or_404, render, redirect
from blog.models import Post, Category
from django.utils import timezone
from django.db.models import Q
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .forms import CongratulationForm
from .models import Congratulation
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()


def profile_user(request, username):
    profile = get_object_or_404(User, username=username)

    posts = Post.objects.filter(author=profile).order_by("-pub_date")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"profile": profile, "page_obj": page_obj}
    for post in context["page_obj"]:
        post.comment_count = Congratulation.objects.filter(
            post_id=post.id
        ).count()
    return render(request, "blog/profile.html", context)


class IndexListView(ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            Post.objects.select_related("category")
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now(),
            )
            .order_by("-pub_date")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for post in context["page_obj"]:
            post.comment_count = Congratulation.objects.filter(
                post_id=post.id
            ).count()
        return context


def post_detail(request, id):
    template = "blog/detail.html"
    post_full = get_object_or_404(Post, pk=id)
    if request.user == post_full.author and not (post_full.is_published):
        post = get_object_or_404(Post, pk=id)
    else:
        post = get_object_or_404(
            Post.objects.select_related("category"),
            Q(pk=id)
            & Q(pub_date__lte=timezone.now())
            & Q(is_published=True)
            & Q(category__is_published=True),
        )
    form = CongratulationForm()
    # congratulations = post.congratulations.select_related('author')
    comments = Congratulation.objects.filter(post=id)

    context = {
        "post": post,
        "form": form,
        # "congratulations": congratulations,
        "comments": comments,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = "blog/category.html"
    category = get_object_or_404(
        Category.objects.filter(slug=category_slug), is_published=True
    )
    post_list = (
        Post.objects.select_related("category")
        .filter(
            category=category, is_published=True, pub_date__lte=timezone.now()
        ).order_by("-pub_date")
    )

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "category": category}
    return render(request, template, context)


@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("blog:profile", username=request.user.username)
    context = {"form": form}
    return render(request, "blog/create.html", context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect("blog:post_detail", id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", id=post_id)
    else:
        form = PostForm(instance=post)
    context = {"post": post, "form": form}
    return render(request, "blog/create.html", context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CongratulationForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect("blog:post_detail", id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Congratulation, pk=comment_id, post=post_id)
    if comment.author == request.user:
        if request.method == "POST":
            form = CongratulationForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect("blog:post_detail", id=post_id)
        else:
            form = CongratulationForm(instance=comment)
    else:
        return redirect("blog:post_detail", id=post_id)

    context = {"comment": comment, "form": form}

    return render(request, "blog/comment.html", context)


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not (request.user == post.author or request.user.is_superuser):
        return redirect("blog:index")

    if request.method == "POST":
        post.delete()
        return redirect("blog:index")

    form = PostForm(instance=post)
    context = {"post": post, "form": form}

    return render(request, "blog/create.html", context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Congratulation, pk=comment_id, post_id=post_id)

    if request.user == comment.author or request.user.is_superuser:
        if request.method == "POST":
            comment.delete()
    else:
        return redirect("blog:post_detail", id=post_id)

    context = {"comment": comment}

    return render(request, "blog/comment.html", context)


class DeleteCommentDeleteView(DeleteView):
    model = Congratulation
    template_name = "blog/comment.html"
    success_url = reverse_lazy("blog:index")

    def get_object(self):
        comment_id = self.kwargs.get("comment_id")
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        return get_object_or_404(Congratulation, pk=comment_id, post_id=post)


class CreateUserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    template_name = "blog/user.html"

    def get_success_url(self):
        return reverse_lazy("blog:profile", kwargs={
            "username": self.object.username
        })

    def get_object(self):
        return self.request.user
