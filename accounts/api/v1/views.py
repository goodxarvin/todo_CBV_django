from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from mail_templated.message import EmailMessage
from jwt import decode
from decouple import config
from jwt.exceptions import ExpiredSignatureError, DecodeError
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    RegistrationSerializer,
    ResetPasswordSerializer,
    CustomTokenObtainPairSerializer,
    ProfileSerializer,
    ForgotPasswordSerializer,
    NewPasswordForgetSerializer,
)
from .utils import EmailThread
from ...models import Profile
from ...tasks import (
    send_email_verification_worker,
    resend_email_verification_worker,
    forgot_password_email_worker,

    )

user = get_user_model()


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        username = serializer.validated_data["username"]
        user_object = user.objects.get(username=username)
        access_token = f"http://127.0.0.1:80/accounts-api/api/v1/verify-account/{self.get_token_for_user(user_object)}"
        send_email_verification_worker.delay(user_object.username, access_token)
        # user_object = user.objects.get(username=username)
        # access_token = f"http://127.0.0.1:8000/accounts-api/api/v1/verify-account/{self.get_token_for_user(user_object)}"
        # email_object = EmailMessage(
        #     subject="test email",
        #     template_name="mail/verification.tpl",
        #     context={"name": username, "access_token": access_token},
        #     from_email="from@a.aa",
        #     to=[
        #         "to@am.am",
        #     ],
        # )

        # email_thread = EmailThread(email_object).start()
        return Response(
            {
                "details": "your account has been created successfully and verification email sent",
                "usersname": username,
            },
            status=status.HTTP_201_CREATED,
        )


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        username = serializer.validated_data["username"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "username": username}, status=status.HTTP_201_CREATED
        )


class DiscardAuthToken(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(
                {"details": "auth token deleted and loged out"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Token.DoesNotExist:
            return Response(
                {"details": "user signed out (auth token not found)"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordAPIView(generics.GenericAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"details": "password changed successfully"})


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["username"] = request.data.get("username")
        try:
            data["email"] = request.user.email
        except AttributeError:
            data["email"] = None
        return Response(data)


class ResendVerificationAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request, *args, **kwargs):
        username = request.user.username
        user_object = user.objects.get(username=username)
        if user_object.is_verified:
            return Response(
                {"details": "resend failed this account has already been verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        access_token = f"http://127.0.0.1:80/accounts-api/api/v1/verify-account/{self.get_token_for_user(user_object)}"
        resend_email_verification_worker.delay(user_object.username, access_token)
        # email_object = EmailMessage(
        #     subject="resend verification email",
        #     template_name="mail/verification_resend.tpl",
        #     context={"name": username, "access_token": access_token},
        #     from_email="from@a.aa",
        #     to=[
        #         "to@am.am",
        #     ],
        # )

        # email_thread = EmailThread(email_object).start()

        return Response({"details": "resent verification email successful"})


class VerificationTokenAPIView(APIView):

    def get(self, request, access_jwt):
        try:
            decoded_jwt = decode(
                access_jwt, config("DJANGO_SECRET_KEY"), algorithms=["HS256"]
            )
            user_id = decoded_jwt["user_id"]
            user_object = user.objects.get(pk=user_id)

            if not user_object.is_verified:
                user_object.is_verified = True
                user_object.save()
            else:
                return Response(
                    {"details": "account has already been verified"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except ExpiredSignatureError:
            return Response(
                {"details": "token expired"}, status=status.HTTP_406_NOT_ACCEPTABLE
            )

        except DecodeError:
            return Response(
                {"details": "invalid signiture"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"details": "your account has been verified successully"})


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class ForgotPasswordAPIView(generics.GenericAPIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = ForgotPasswordSerializer

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_object = serializer.validated_data["user"]
        # print("-------------------------------", username)
        # user_object = user.objects.get(username=username)
        access_token = f"http://127.0.0.1:80/accounts-api/api/v1/new-password/{self.get_token_for_user(user_object)}"
        forgot_password_email_worker.delay(user_object.username, access_token)
        # email_object = EmailMessage(
        #     subject="forgot password email",
        #     template_name="mail/forgot_password.tpl",
        #     context={"name": user_object.username, "access_token": access_token},
        #     from_email="from@a.aa",
        #     to=[
        #         "to@am.am",
        #     ],
        # )
        # email_thread = EmailThread(email_object).start()

        return Response({"details": "resent reset password url successful"})


class NewPasswordForgotAPIView(generics.GenericAPIView):
    serializer_class = NewPasswordForgetSerializer

    def post(self, request, *args, **kwargs):
        try:
            jwt_info = decode(
                kwargs["reset_pass_jwt"],
                config("DJANGO_SECRET_KEY"),
                algorithms=["HS256"],
            )
            user_id = jwt_info.get("user_id")
            user_object = user.objects.get(pk=user_id)
            serializer = self.get_serializer(user_object, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except ExpiredSignatureError:
            return Response(
                {"details": "password reset token expired"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        except DecodeError:
            return Response(
                {"details": "invalid signiture"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"details": "password changed successfully"})
