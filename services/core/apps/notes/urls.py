from django.urls import path, include
from rest_framework.routers import DefaultRouter
from notes import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'blocks', views.BlockViewSet,basename="blocks")
router.register(r'users', views.UserViewSet,basename="users")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', views.editorjs_view),
    path('editorjs_posting/', views.update_blocks),
    path('editorjs_getting/', views.get_blocks)
]