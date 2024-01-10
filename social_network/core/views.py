from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from social_network.core.models import PostLike

from social_network.core.serializers import PostLikeSerializer, PostSerializer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_post(request):
    request.data["author"] = request.user.pk
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def post_like(request, post_id):
    user_id = request.user.pk
    data = {"user_id": user_id, "post_id": post_id}
    serializer = PostLikeSerializer(data=data)
    if serializer.is_valid():
        like_filter = PostLike.objects.filter(post_id=post_id, user_id=user_id).first()
        if not like_filter:
            serializer.save()
            return Response(f"Post {post_id} liked successfully", status=status.HTTP_201_CREATED)
        else:
            like_filter.delete()
            return Response(f"Post {post_id} unliked successfully", status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
