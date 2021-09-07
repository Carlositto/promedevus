from django.urls import path
from .views import HomePage, PostCreate, PostAttachmentCreate

urlpatterns = [
    path('', HomePage.as_view(), name='home-page'),
    path('post/create/', PostCreate.as_view(), name='post-create'),
    path('post/attachment/create/', PostAttachmentCreate.as_view(), name='post-attachment-create'),
]
