from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ChooseAuthView.as_view(), name='choose_auth'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('post_list', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:post_id>/toggle_like/', views.like_post, name='toggle_like'), 
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='diary/password_change/my_password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='diary/password_change/my_password_change_done.html'), name='password_change_done'),
]
