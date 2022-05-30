from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers

from notes.views import BlockViewSet, UserViewSet, api_root


block_list = BlockViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
block_detail = BlockViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

# API endpoints
urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('blocks/', block_list, name='block-list'),
    path('blocks/<int:pk>/', block_detail, name='block-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])