from rest_framework import serializers

from .models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_is_liked(self, object) -> bool:
        return PostLike.objects.filter(
            user_id=object.author, post_id=object.id
        ).exists()


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"


class PostCreateSerializer(serializers.Serializer):
    body = serializers.CharField()
    title = serializers.CharField()


class PostLikeAnalyticsSerializer(serializers.Serializer):
    date = serializers.DateField(source="created_at__date")
    likes_count = serializers.IntegerField()
