from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Relation, Profile


class UserSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'following_count', 'followers_count')


    def get_following_count(self, obj):
        following = obj.following.count()
        return following

    def get_followers_count(self, obj):
        followers = obj.followers.count()
        return followers


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password','password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError('username cant be admin')
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('passwords must match')
        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'age', 'address')
        read_only_fields = ('user',)
