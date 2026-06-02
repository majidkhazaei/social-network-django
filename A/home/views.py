from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.post_instance.pcomments.filter(is_reply=False)
        return render(request, 'home/detail.html', {
            'post': self.post_instance,
            'comments': comments,'form': self.form_class,
            'reply_form': self.form_class_reply,
        })

    @method_decorator(login_required)
    def post(self,request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request,'comment saved...','success')
            return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)


class PostDeleteView(LoginRequiredMixin,View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'پست با موفقیت حذف شد.','success')
        else:
            messages.error(request, 'شما نمی توانید این پست را حذف کنید','danger')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(id=kwargs['post_id'])
        return super().setup(request,*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'شما نمی توانید این پست را ویرایش کنید!', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'پست ویرایش شد.', 'success')
            return redirect('home:post_detail', post.id, post.slug)


class PostCreateView(LoginRequiredMixin,View):
    form_class = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        return render(request, 'home/create.html', {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['body'][:20])
            new_post.save()
            messages.success(request,'پست با موفقیت ایجاد شد','success')
            return redirect('home:post_detail', new_post.id, new_post.slug)


class PostAddReplyView(LoginRequiredMixin,View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = Post.objects.get(pk=post_id)
        comment = Comment.objects.get(pk=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request,'reply added...','success')
        return redirect('home:post_detail', post.id, post.slug)


