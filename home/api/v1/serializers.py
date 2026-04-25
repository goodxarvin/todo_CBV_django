from rest_framework import serializers
from ...models import Objective


class ObjectiveSerializer(serializers.ModelSerializer):

    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_absolute_url")

    class Meta:
        model = Objective
        fields = ["id", "title", "snippet", "description", "status", "owner", "relative_url", "absolute_url", "created_at", "updated_at"]
        read_only_fields = ["id", "owner", "absolute_url", "relative_url", "created_at"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs"):
            rep.pop("relative_url")
            rep.pop("absolute_url")
            rep.pop("description")
        else:
            rep.pop("description")
        return rep
    
    def create(self, validated_data):
        validated_data["owner"] = self.context.get("request").user
        return super().create(validated_data)