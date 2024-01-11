from rest_framework import serializers
from .models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'


class PostLikeAnalyticsSerializer(serializers.Serializer):
    date = serializers.DateField(source='created_at__date')
    likes_count = serializers.IntegerField()