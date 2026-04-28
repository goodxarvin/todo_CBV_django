
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import (
    RegistrationSerializer,
    ResetPasswordSerializer
)

class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        username = serializer.validated_data["username"]
        return Response({"usersname": username}, status=status.HTTP_201_CREATED)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        username = serializer.validated_data["username"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, "username": username}, status=status.HTTP_201_CREATED)



class DiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"details": "auth token deleted and loged out"}, status=status.HTTP_204_NO_CONTENT)
        except Token.DoesNotExist:
            return Response({"details": "user signed out (auth token not found)"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"details": "password changed successfully"})