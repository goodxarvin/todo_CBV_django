from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Any
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from ...models import User, Profile
class RegistrationSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            serializers.ValidationError({"details": "passwords aren't match"})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"details": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)


class ResetPasswordSerializer(serializers.Serializer):
    old_pass = serializers.CharField(write_only=True, required=True)
    new_pass = serializers.CharField(write_only=True, required=True)
    confirm_pass = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        request = self.context.get("request")
        if attrs.get("new_pass") != attrs.get("confirm_pass"):
            raise serializers.ValidationError({"details": "password doesn't match"})
        
        elif not request.user.check_password(attrs.get("old_pass")):
            raise serializers.ValidationError({"details": "wrong password"})

        try:
            validate_password(attrs.get("new_pass"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"details": list(e.messages)})
        
        return super().validate(attrs)

    def update(self, instance, validated_data):
        new_pass = validated_data["new_pass"]
        instance.set_password(new_pass)
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "country", "phone", "username"]


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"details": "this username does not exist"})

        attrs["user"] = user
        return attrs


class NewPasswordForgetSerializer(serializers.Serializer):
    new_pass = serializers.CharField(required=True, write_only=True)
    confirm_pass = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        new_pass = attrs.get("new_pass")
        confirm_pass = attrs.get("confirm_pass")
        if new_pass != confirm_pass:
            raise serializers.ValidationError({"details": "passwords does not match"})
        elif not not self.instance.check_password(new_pass):
            raise serializers.ValidationError({"details": "this is already your password"})
        try:
            validate_password(new_pass)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"details:": list(e.messages)})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        new_pass = validated_data["new_pass"]
        instance.set_password(new_pass)
        instance.save()
        return instance

# class VerificationTokenSerializer(serializers.Serializer):

#     access_token = serializers.CharField()

#     def validate(self, attrs):
#         access_token = attrs.get("access_token")
#         print("------------------------------------------", attrs, "--------------------------------------")
#         return "ok"