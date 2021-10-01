import markdown
import os
import json
import uuid

from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, CreateView, FormView, ListView, DetailView, UpdateView, View
from django.views.generic.detail import SingleObjectMixin
from .forms import PostForm, AttachmentFormset




from martor_markdown_plus.utils import LazyEncoder



class HomePage(TemplateView):
    template_name = "devblog/home_page.html"


class PostCreate(CreateView):
    template_name = "devblog/post_create.html"
    model = apps.get_model('devblog.Post')
    fields = '__all__'


class PostAttachmentCreate(CreateView):#, SingleObjectMixin):
    template_name = "devblog/post_attachment_create.html"
    model = apps.get_model('devblog.Post')
    #form_class = PostForm(request.POST)
    #fields = '__all__'

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
        #form_class = PostForm(self.request.POST)
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


class PostDetail(DetailView):
    template_name = "devblog/post_detail.html"
    model = apps.get_model('devblog.Post')


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        md = markdown.Markdown(extensions=['toc'])
        converted_body = md.convert(self.object.body)
        if apps.get_model('auth.User').objects.filter(id=self.request.user.id).exists():
            context['liked'] = apps.get_model('devblog.Like').objects.filter(user=self.request.user, post=self.get_object()).exists()
        #context['post_body'] = converted_body
        context['toc'] = md.toc
        context['toc_tokens'] = md.toc_tokens
        context['attachments'] = apps.get_model('devblog.PostAttachment').objects.filter(post=self.object)
        return context

class PostUpdate(UpdateView):
    template_name = "devblog/post_update.html"
    model = apps.get_model('devblog.Post')
    form_class = PostForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['attachment_form'] = AttachmentFormset(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        #form_class = PostForm(self.request.POST)
        form = PostForm(self.request.POST, instance=self.get_object())
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
        if not apps.get_model('devblog.Like').objects.filter(post=post).exists():
            apps.get_model('devblog.Like').objects.create(user=self.request.user, post=post)
            data['liked'] = 1
        else:
            apps.get_model('devblog.Like').objects.get(user=self.request.user, post=post).delete()
            data['liked'] = 0
        return JsonResponse(data)


