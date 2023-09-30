import markdown

from django.apps import apps
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, FormView, ListView, DetailView, UpdateView, View
from .forms import PostForm, AttachmentFormset

class PostAttachmentCreate(PermissionRequiredMixin, CreateView):
    template_name = "devblog/post_attachment_create.html"
    model = apps.get_model('devblog.Post')
    permission_required = ('devblog.change_post', 'devblog.create_post')

    def get(self, request, *args, **kwargs):
        self.object = None
        form = PostForm()
        attachment_form = AttachmentFormset()
        return self.render_to_response(
            self.get_context_data(
                form=form,
                attachment_form=attachment_form
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form = PostForm(self.request.POST)
        attachment_form = AttachmentFormset(self.request.POST, self.request.FILES)
        if (form.is_valid() and attachment_form.is_valid()):
            return self.form_valid(form, attachment_form)
        else:
            return self.form_invalid(form, attachment_form)

    def form_valid(self, form, attachment_form):
        self.object = form.save()
        attachment_form.instance = self.object
        attachment_form.save()
        return HttpResponseRedirect(self.get_success_url(self.object))


    def form_invalid(self, form, attachment_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                attachment_form=attachment_form,
            )
        )

    def get_success_url(self, form_object):
        return reverse_lazy('post-detail', args=[form_object.id])


class PostsList(ListView):
    template_name = "devblog/posts_list.html"
    model = apps.get_model('devblog.Post')
    queryset = apps.get_model('devblog.Post').objects.filter(is_published=True)


class AdminPostsList(PermissionRequiredMixin, ListView):
    template_name = "devblog/admin_posts_list.html"
    model = apps.get_model('devblog.Post')
    # permission_required = 'devblog.change_post'

    def has_permission(self):
        return self.request.user.is_superuser


class PostDetail(DetailView):
    template_name = "devblog/post_detail.html"
    model = apps.get_model('devblog.Post')


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        md = markdown.Markdown(extensions=['toc'])
        converted_body = md.convert(self.object.body)
        if apps.get_model('auth.User').objects.filter(id=self.request.user.id).exists():
            content_type = apps.get_model('contenttypes.ContentType').objects.get(model='post')
            context['liked'] = apps.get_model('devblog.Like').objects.filter(user=self.request.user, target_type=content_type, target_id=self.get_object().id).exists()
        #context['post_body'] = converted_body
        context['toc'] = md.toc
        context['toc_tokens'] = md.toc_tokens
        context['attachments'] = apps.get_model('devblog.PostAttachment').objects.filter(post=self.object)
        return context


class BlogUserDetail(DetailView):
    template_name = "devblog/blog_user_detail.html"
    model = apps.get_model('blog_users.BlogUser')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        content_type = apps.get_model('contenttypes.ContentType').objects.get(model='post')
        related_posts = apps.get_model('django_comments.Comment').objects.filter(user=self.request.user).order_by().values_list('object_pk', flat=True).distinct()
        posts_ids = [int(pk) for pk in related_posts]
        context['posts_participated'] = apps.get_model('devblog.Post').objects.filter(id__in=posts_ids)
        context['liked_posts'] = apps.get_model('devblog.Like').objects.filter(user=self.object.user, target_type=content_type)
        return context


class BlogUserUpdate(UpdateView):
    template_name = "devblog/bloguser_form.html"
    model = apps.get_model('blog_users.BlogUser')
    fields = ['profile_image', 'first_name', 'last_name', 'email', 'description']

    def get_success_url(self):
        return reverse_lazy('blog-user-detail', args=[self.kwargs['pk']])


class PostUpdate(PermissionRequiredMixin, UpdateView):
    template_name = "devblog/post_update.html"
    model = apps.get_model('devblog.Post')
    form_class = PostForm
    permission_required = 'devblog.change_post'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['attachment_form'] = AttachmentFormset(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #form_class = PostForm(self.request.POST)
        #form = PostForm(self.request.POST, instance=self.get_object())
        attachment_form = AttachmentFormset(self.request.POST, self.request.FILES, instance=self.object)
        if (form.is_valid() and attachment_form.is_valid()):
            return self.form_valid(form, attachment_form)
        else:
            return self.form_invalid(form, attachment_form)

    def form_valid(self, form, attachment_form):
        form.save()
        attachment_form.save()
        return HttpResponseRedirect(self.get_success_url())


    def form_invalid(self, form, attachment_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                attachment_form=attachment_form,
            )
        )

    def get_success_url(self):
        return reverse_lazy('post-detail', args=[self.kwargs['pk']])


class PostLike(View):

    def post(self, request, pk):
        data = {}
        post = apps.get_model('devblog.Post').objects.get(id=self.kwargs['pk'])
        content_type = apps.get_model('contenttypes.ContentType').objects.get(model='post')
        if not apps.get_model('devblog.Like').objects.filter(target_type=content_type, target_id=post.id, user=self.request.user).exists():
            apps.get_model('devblog.Like').objects.create(user=self.request.user, target_type=content_type, target_id=post.id)
            data['liked'] = 1
        else:
            apps.get_model('devblog.Like').objects.get(user=self.request.user, target_type=content_type, target_id=post.id).delete()
            data['liked'] = 0
        return JsonResponse(data)


class CommentLike(View):

    def post(self, request, pk):
        data = {}
        comment = apps.get_model('django_comments.Comment').objects.get(id=self.kwargs['pk'])
        content_type = apps.get_model('contenttypes.ContentType').objects.get(model='comment', app_label='django_comments')
        if not apps.get_model('devblog.Like').objects.filter(target_type=content_type, target_id=comment.id, user=self.request.user).exists():
            apps.get_model('devblog.Like').objects.create(user=self.request.user, target_type=content_type, target_id=comment.id)
            data['liked'] = 1
        else:
            apps.get_model('devblog.Like').objects.get(user=self.request.user, target_type=content_type, target_id=comment.id).delete()
            data['liked'] = 0
        return JsonResponse(data)


class LoadComments(View):

    def get(self, request):
        detail_object = apps.get_model('devblog.Post').objects.get(id=self.request.GET['object_pk'])
        context = {'object': detail_object, 'sort_by': self.request.GET['sort_by']}
        return render(request, 'devblog/load_comments.html', context=context)


class AboutTemplate(TemplateView):
    template_name = "devblog/about.html"


class PostPublish(View):
    def get(self, request, *args, **kwargs):
        post = apps.get_model('devblog.Post').objects.get(id=kwargs['post_id'])
        post.publish_post()
        return redirect('admin-posts-list')


class PostHide(View):
    def get(self, request, *args, **kwargs):
        post = apps.get_model('devblog.Post').objects.get(id=kwargs['post_id'])
        post.hide_post()
        return redirect('admin-posts-list')
