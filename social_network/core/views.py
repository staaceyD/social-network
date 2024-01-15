from django.db.models import Count
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from social_network.core.models import Post, PostLike
from social_network.core.serializers import (
    PostCreateSerializer,
    PostLikeAnalyticsSerializer,
    PostLikeSerializer,
    PostSerializer,
)


@extend_schema_view(
    get=extend_schema(
        description="Returns a list of Post model instances.", responses=PostSerializer
    ),
    post=extend_schema(
        description="Creates a new post by authenticated user",
        request=PostCreateSerializer,
        responses=PostSerializer,
    ),
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def posts(request):
    if request.method == "POST":
        request.data["author"] = request.user.pk
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "GET":
        user = request.user
        posts = Post.objects.filter(author=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_like(request, post_id):
    """
    Creates a like on the post
    """
    user_id = request.user.pk
    post = Post.objects.get(id=post_id)
    post.likes_number += 1
    data = {"user_id": user_id, "post_id": post_id}
    serializer = PostLikeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        post.save()
        return Response(
            {"message": f"Post {post_id} liked successfully"},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def post_dislike(request, post_id):
    """
    Removes the like user gave the post
    """
    user_id = request.user.pk
    like_filter = PostLike.objects.filter(post_id=post_id, user_id=user_id).first()
    post = Post.objects.get(id=post_id)
    if post.likes_number > 0:
        post.likes_number -= 1
    else:
        return Response(
            {"message": "The post cannot be disliked. Post was never liked"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if like_filter:
        like_filter.delete()
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {"message": "The post cannot be disliked. Like was not found"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@extend_schema(
    parameters=[
        OpenApiParameter(name="date_from", description="Category Id", type=str),
        OpenApiParameter(name="date_to", description="Category Id", type=str),
    ],
    responses={200: PostLikeAnalyticsSerializer},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def post_like_analytics(request):
    """
    Takes dates range in params to return the amount of likes made that day grouped by dates
    """
    date_from = request.query_params.get("date_from")
    date_to = request.query_params.get("date_to")

    queryset = (
        PostLike.objects.filter(created_at__range=(date_from, date_to))
        .values("created_at__date")
        .annotate(likes_count=Count("id"))
    )

    serializer = PostLikeAnalyticsSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
