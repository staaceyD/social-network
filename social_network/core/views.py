from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from social_network.core.models import PostLike

from social_network.core.serializers import PostLikeAnalyticsSerializer, PostLikeSerializer, PostSerializer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_post(request):
    request.data["author"] = request.user.pk
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_like(request, post_id):
    user_id = request.user.pk
    data = {"user_id": user_id, "post_id": post_id}
    serializer = PostLikeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(f"Post {post_id} liked successfully", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def post_dislike(request, post_id):
    user_id = request.user.pk
    like_filter = PostLike.objects.filter(post_id=post_id, user_id=user_id).first()

    if like_filter:
        like_filter.delete()
        return Response(f"Post {post_id} disliked successfully", status=status.HTTP_200_OK)
    return Response("The post cannot be disliked. Like was not found", status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def post_like_analytics(request):
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to')

    queryset = PostLike.objects.filter(
        created_at__range=(date_from, date_to)
    ).values('created_at__date').annotate(likes_count=Count('id'))

    serializer = PostLikeAnalyticsSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
