from rest_framework import serializers
from .models import Post, Comment, Profile
from likes.models import Like
from django.contrib.auth import get_user_model

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
        # user = self.context['request'].user
        user = User.objects.get(pk=1)
        post_id = self.context['post_pk']
        content = validated_data['content']

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

    def get_likes(self, instance):

        likes_count = Like.objects.get_likes_count(instance, instance.pk)
        print(f"Likes count: {likes_count}")
        return likes_count

    class Meta:
        model = Post
        fields = ['pk', 'author', 'title', 'content', 'created_date', 'modified_date', 'is_published', 'likes']
        read_only_fields = ['author', 'created_date', 'modified_date']


    def create(self, validated_data):
        instance = Post(**validated_data)
        return instance