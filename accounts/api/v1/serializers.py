from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from ...models import User


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
            raise serializers.ValidationError({"details": "wring password"})

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
