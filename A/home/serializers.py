from .models import Post, Comment
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    user_likes = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user','slug', 'created', 'updated')

    def get_like_count(self, obj):
        return obj.plikes.count()

    def get_comment_count(self, obj):
        return obj.pcomments.count()

    def get_user_likes(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user_likes(request.user)
        return False


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'body', 'created','is_reply', 'reply')
        read_only_fields = ('user', 'post',' created', 'is_reply', 'reply')

    def get_replies(self, obj):
        if not obj.is_reply:
            return CommentSerializer(obj.rcomments.all(), many=True, context=self.context).data
        return []

    def validate_body(self, body):
        if not body or body.strip() == '':
            raise serializers.ValidationError('Body cannot be an empty string')
        return body
