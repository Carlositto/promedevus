import datetime

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from martor_markdown_plus.models import MartorField

TARGET_MODELS = ['post', 'comment']

class Post(models.Model):
    title = models.CharField(max_length=64, verbose_name='Title')
    subtitle = models.CharField(max_length=32, verbose_name='Subtitle', blank=True)
    short_description = models.CharField(max_length=128, verbose_name='Short description', help_text='This is the text usually shown in the menu or on hover')
    body = MartorField(verbose_name='Main body')
    authors = models.ManyToManyField('Author', verbose_name='Authors of the article', through='PostAuthor', blank=True)
    tags = models.ManyToManyField('Tag', verbose_name='Tags realted to the article', through='PostTag', blank=True)
    category = models.ManyToManyField('Category', verbose_name='Category', through='PostCategory', blank=True)
    date_created = models.DateField(verbose_name='Publication date', default=datetime.date.today())


class Tag(models.Model):
    name = models.CharField(max_length=16, verbose_name="Tag's name")
    description = models.CharField(max_length=128, verbose_name="Tag's short description", help_text='This is the description shown on hover')


class PostTag(models.Model):
    tag = models.ForeignKey('Tag', verbose_name='Tag', on_delete=models.CASCADE, related_name='tags')
    post = models.ForeignKey('Post', verbose_name='Post', on_delete=models.CASCADE, related_name='post_tags')


class Author(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class PostAuthor(models.Model):
    author = models.ForeignKey('Author', verbose_name="Post's author", on_delete=models.CASCADE, related_name='authors')
    post = models.ForeignKey('Post', verbose_name='Post', on_delete=models.CASCADE, related_name='post_authors')


class Category(models.Model):
    name = models.CharField(max_length=16, verbose_name="Category's name")
    description = models.CharField(max_length=128, verbose_name="Short description")


class PostCategory(models.Model):
    category = models.ForeignKey('Category', verbose_name="Post's category", on_delete=models.CASCADE, related_name='categories')
    post = models.ForeignKey('Post', verbose_name='Post', on_delete=models.CASCADE, related_name='post_categories')


class PostAttachment(models.Model):
    attachment = models.FileField()
    post = models.ForeignKey('Post', verbose_name='Post', on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.attachment


class Like(models.Model):
    post = models.ForeignKey('Post', verbose_name='Post', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    target_type = models.ForeignKey(ContentType, limit_choices_to={'model__in': TARGET_MODELS}, on_delete=models.PROTECT)
    target_id = models.PositiveIntegerField()
    target_object = GenericForeignKey('target_type', 'target_id')


class GenericComment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    comment_body = models.TextField(verbose_name='Comment body')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Comment(GenericComment):
    post = models.ForeignKey('Post', verbose_name='Post', on_delete=models.CASCADE, related_name='comments')


class Reply(GenericComment):
    comment = models.ForeignKey('Comment', verbose_name='Comment', on_delete=models.CASCADE, related_name='replies')

