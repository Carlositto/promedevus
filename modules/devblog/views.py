from django.apps import apps
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from .forms import PostForm, AttachmentFormset

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
        return HttpResponseRedirect(self.get_success_url())


    def form_invalid(self, form, attachment_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                attachment_form=attachment_form,
            )
        )

    def get_success_url(self):
        return reverse_lazy('home-page')


class PostsList(ListView):
    template_name = "devblog/posts_list.html"
    model = apps.get_model('devblog.Post')


class PostDetail(DetailView):
    template_name = "devblog/post_detail.html"
    model = apps.get_model('devblog.Post')
