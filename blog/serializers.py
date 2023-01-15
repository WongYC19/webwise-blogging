from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import status

from .models import Post, Comment, Profile
from likes.models import Like

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'first_name', 'last_name', 'birth_date', 'phone_number', 'github_link', 'linkedin_link']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ['pk', 'user', 'post', 'content', 'created_date', 'modified_date', 'likes']
        read_only_fields = ["pk", "post", 'likes', 'created_date', 'modified_date', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        post_id = self.context['post_pk']
        content = validated_data['content']

        if user.is_anonymous:
            res = serializers.ValidationError("Please get the authentication before making comment to a post.")
            res.status_code = status.HTTP_401_UNAUTHORIZED
            raise res

        if not user.is_staff:
            try:
                Post.objects.get(pk=post_id, is_published=True)
            except Post.DoesNotExist:
                res = serializers.ValidationError("The post is inaccessible or not existed.")
                res.status_code = status.HTTP_403_FORBIDDEN
                raise res
            except Exception as error:
                raise serializers.ValidationError(f"{error}")

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError(f"The `post` {post_id} doesn't exist.")

        instance = Comment.objects.create(user=user, post=post, content=content)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_likes(self, instance):
        likes_count = Like.objects.get_likes_count(instance, instance.pk)
        return likes_count

    def get_comments(self, instance):
        view = self.context.get('view')
        if view and view.action ==  'retrieve':
            serializer = CommentSerializer(instance.comments.all(), many=True, read_only=True)
            return serializer.data
        return None
    class Meta:
        model = Post
        fields = ['pk', 'author', 'title', 'content', 'created_date', 'modified_date', 'is_published', 'likes', 'comments']
        read_only_fields = ['pk', 'author', 'created_date', 'modified_date', 'likes', 'comments']

    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs