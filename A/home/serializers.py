from .models import Post
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    user_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user','slug', 'created', 'updated')

    def get_like_count(self, obj):
        return obj.plikes.count()

    def get_user_likes(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user_likes(request.user)
        return False
