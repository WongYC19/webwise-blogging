from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

from rest_framework import status
from rest_framework import serializers

from .models import Post, Comment, Profile
from likes.models import Like

from tags.models import TaggedItem
from tags.serializers import TaggedItemSerializer

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'first_name', 'last_name', 'birth_date', 'phone_number', 'github_link', 'linkedin_link']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['pk', 'user', 'post', 'content', 'created_date', 'modified_date', 'likes']
        read_only_fields = ["pk", "post", 'likes', 'created_date', 'modified_date', 'user']

    def get_likes(self, instance):
        likes_count = Like.objects.get_likes_count(instance, instance.pk)
        return likes_count

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        post_id = self.context['post_pk']

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
    title = serializers.CharField(validators=[MinLengthValidator(3, message="Please input at least 3 characters for title.")])
    content = serializers.CharField(validators=[MinLengthValidator(3, message="Please input at least 3 characters for content.")])
    # tags = TaggedItemSerializer(many=True, read_only=True)
    tags = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    def get_tags(self, instance):
        tagged_item = TaggedItem.objects.get_tags_for(instance, instance.pk)
        serializer = TaggedItemSerializer(tagged_item)
        return serializer.data.get('tag', [])

    def get_comments(self, instance):
        view = self.context.get('view')
        if view and view.action ==  'retrieve':
            serializer = CommentSerializer(instance.comments.all(), many=True, read_only=True)
            return serializer.data
        return None

    def get_likes(self, instance):
        likes_count = Like.objects.get_likes_count(instance, instance.pk)
        return likes_count

    def validate(self, attrs):
    #     # super().validate(attrs)
        attrs['author'] = self.context['request'].user
        return attrs

    class Meta:
        model = Post
        fields = ['pk', 'author', 'title', 'content', 'created_date', 'modified_date', 'is_published', 'tags', 'comments', 'likes',]
        read_only_fields = ['pk', 'author', 'created_date', 'modified_date', 'comments', 'likes',]


