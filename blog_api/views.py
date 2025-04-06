from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import BlogPost
from .serializers import BlogPostSerializer, RegisterSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly

# Blog Post ViewSet (Handles List, Create, Retrieve, Update, Destroy)
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    # Apply permissions: ReadOnly for anyone, Write only for authenticated users, Edit/Delete only for author
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # Override perform_create to associate the post with the logged-in user
    # This is an alternative to doing it in the serializer's create method
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

# Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,) # Anyone can register
    serializer_class = RegisterSerializer

# Custom Login View (inherits from DRF's ObtainAuthToken)
# This allows customizing the response if needed (e.g., include user details)
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user) # Serialize user data
        return Response({
            'token': token.key,
            'user': user_serializer.data # Include user details in login response
        })

# Optional: View to get current user details based on token
class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user