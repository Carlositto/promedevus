from django.urls import path
from .views import HomePage, PostCreate, PostAttachmentCreate, PostsList, PostDetail

urlpatterns = [
    path('', HomePage.as_view(), name='home-page'),
    path('post/create/', PostCreate.as_view(), name='post-create'),
    path('post/attachment/create/', PostAttachmentCreate.as_view(), name='post-attachment-create'),
    path('posts/list/', PostsList.as_view(), name='posts-list'),
    path('post/detail/<int:pk>', PostDetail.as_view(), name='post-detail'),
]
