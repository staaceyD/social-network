from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from social_network.auth.models import UserLastRequest

from social_network.auth.serializers import RegisterSerializer

@api_view(["POST"])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_activity_view(request):
    user = request.user
    last_request = UserLastRequest.objects.get_or_create(user=user)[0]
    last_login = User.objects.get(id=user.id).last_login

    return Response({'last_request_at': last_request.last_request_at, 'last_login_at': last_login})