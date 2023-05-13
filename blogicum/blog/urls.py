from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path(
        'posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'
    ),
    path(
        'posts/<int:pk>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post',
    ),
    path(
        'posts/<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post',
    ),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path(
        'category/<slug:category_slug>/',
        views.CategoryListView.as_view(),
        name='category_posts',
    ),
    path(
        'profile/<slug:username>/', views.ProfileView.as_view(), name='profile'
    ),
    path('edit_profile/', views.ProfileUpdate.as_view(), name='edit_profile'),
    path(
        'posts/<int:pk>/comment/',
        views.CommentAddView.as_view(),
        name='add_comment',
    ),
    path(
        'posts/<int:pk>/edit_comment/<int:id>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment',
    ),
    path(
        'posts/<int:pk>/delete_comment/<int:id>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment',
    ),
]
