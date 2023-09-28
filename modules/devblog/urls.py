from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import PostAttachmentCreate, PostsList, PostDetail, PostUpdate, PostLike, LoadComments, CommentLike, BlogUserDetail, BlogUserUpdate, AboutTemplate, PostPublish, PostHide, AdminPostsList

urlpatterns = [
    path('', PostsList.as_view(), name='posts-list'),
    path('about/', AboutTemplate.as_view(), name='about-page'),
    path('post/attachment/create/', PostAttachmentCreate.as_view(), name='post-attachment-create'),
    path('admin-posts/list/', AdminPostsList.as_view(), name='admin-posts-list'),
    path('post/detail/<int:pk>', PostDetail.as_view(), name='post-detail'),
    path('blog-user/detail/<int:pk>', BlogUserDetail.as_view(), name='blog-user-detail'),
    path('blog-user/update/<int:pk>', BlogUserUpdate.as_view(), name='blog-user-update'),
    path('post/update/<int:pk>', PostUpdate.as_view(), name='post-update'),
    path('post/publish/<int:post_id>', PostPublish.as_view(), name='post-publish'),
    path('post/hide/<int:post_id>', PostHide.as_view(), name='post-hide'),
    path('post/like/<int:pk>',login_required(PostLike.as_view()), name='post-like'),
    path('comment/like/<int:pk>',login_required(CommentLike.as_view()), name='comment-like'),
    path('load/comments',LoadComments.as_view(), name='load-comments'),
]
