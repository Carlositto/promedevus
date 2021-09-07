from django import forms
from django.forms import ModelForm
from django.db import models
from django.forms.models import inlineformset_factory
from .models import Post, PostAttachment, Tag, Author
from django_select2.forms import ModelSelect2MultipleWidget

class AuthorWidget(ModelSelect2MultipleWidget):
    search_fields = [
        "user__username__icontains",
    ]

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            "authors": AuthorWidget(attrs={'style': 'width:1000px'}),

        }
    #authors = forms.ModelMultipleChoiceField(
    #    queryset=Author.objects.all(),
    #    widget=ModelSelect2MultipleWidget
    #)



AttachmentFormset = inlineformset_factory(Post, PostAttachment, fields=('attachment',), extra=1, can_delete=True)
