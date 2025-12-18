from django.urls import path
from . import views

app_name = "blog"

name_ed = "edit_profile"
name_add = "add_comment"
cat_p = "category_posts"

urlpatterns = [
    path("profile/edit/", views.CreateUserUpdateView.as_view(), name=name_ed),
    path(
        "posts/<int:post_id>/delete_comment/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment",
    ),
    path(
        "posts/<int:post_id>/edit_comment/<int:comment_id>/",
        views.edit_comment,
        name="edit_comment",
    ),
    path("posts/<int:post_id>/comment/", views.add_comment, name=name_add),
    path("posts/<int:post_id>/delete/", views.delete_post, name="delete_post"),
    path("posts/<int:post_id>/edit/", views.post_edit, name="edit_post"),
    path("posts/create/", views.create_post, name="create_post"),
    path("", views.IndexListView.as_view(), name="index"),
    path("posts/<int:id>/", views.post_detail, name="post_detail"),
    path("category/<slug:category_slug>/", views.category_posts, name=cat_p),
    path("profile/<str:username>/", views.profile_user, name="profile"),
]
