from django.urls import reverse_lazy
from django.views import View, generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .models import Post, Like
from .forms import PostForm
from django.db.models import Q 



# ユーザー登録ビュー
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# ログインビュー（Djangoのデフォルトビューを使用）
class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # ログアウト後にリダイレクトするURL

# 投稿リストビュー
class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'diary/post_list.html'

    def get_queryset(self):
        # ログインユーザーによる投稿、もしくは公開されている投稿のみを返す
        return Post.objects.filter(
            Q(user=self.request.user) | Q(is_public=True)
        )

# 投稿詳細ビュー
class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'diary/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        user_likes_post = post.likes.filter(id=self.request.user.id).exists()  # いいねのチェック
        context['user_likes_post'] = user_likes_post  # テンプレートに渡す
        return context

# 投稿作成ビュー
class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')
    template_name = 'diary/post_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  # 投稿者としてログインユーザーを設定
        return super().form_valid(form)

# 投稿更新ビュー
class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'diary/post_form.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

# 投稿削除ビュー
class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'diary/post_confirm_delete.html'

# いいね機能のビュー
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()  # いいねが既にあれば削除
    return redirect('post_detail', pk=post_id)  # 投稿の詳細ページにリダイレクト