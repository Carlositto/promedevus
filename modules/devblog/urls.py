from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import HomePage, PostCreate, PostAttachmentCreate, PostsList, PostDetail, PostUpdate, PostLike

urlpatterns = [
    path('', HomePage.as_view(), name='home-page'),
    path('post/create/', PostCreate.as_view(), name='post-create'),
    path('post/attachment/create/', PostAttachmentCreate.as_view(), name='post-attachment-create'),
    path('posts/list/', PostsList.as_view(), name='posts-list'),
    path('post/detail/<int:pk>', PostDetail.as_view(), name='post-detail'),
    path('post/update/<int:pk>', PostUpdate.as_view(), name='post-update'),
    path('post/like/<int:pk>',login_required(PostLike.as_view()), name='post-like'),
]
