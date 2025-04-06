from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogPost

# User Serializer (for displaying author info, read-only)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] # Only show necessary fields

# Blog Post Serializer
class BlogPostSerializer(serializers.ModelSerializer):
    # Make author field read-only in list/detail views, but set automatically on create
    author = UserSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] # Ensure these aren't directly editable

    # Automatically set the author to the logged-in user on creation
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

# User Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password", style={'input_type': 'password'})
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        # You can add more password complexity validation here if needed
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Optionally create a token upon registration here if desired
        # from rest_framework.authtoken.models import Token
        # Token.objects.create(user=user)
        return user