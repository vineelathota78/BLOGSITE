from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, RegisterView, CustomAuthToken, UserDetailView

router = DefaultRouter()
router.register(r'blogs', BlogPostViewSet, basename='blogpost')
# The basename is important if your queryset is customized or not standard

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user-detail'), # Endpoint to get current user
    # Add other API paths here (e.g., logout if implemented)
]