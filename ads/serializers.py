from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from ads.models import Ad, Category, Selection
from users.models import User


class AdSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Ad


class AdListSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field="username", queryset=User.objects.all())
    category = SlugRelatedField(slug_field="name", queryset=Category.objects.all())

    class Meta:
        fields = "__all__"
        model = Ad


class SelectionSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Selection


class SelectionDetailSerializer(ModelSerializer):
    items = AdSerializer(many=True)

    class Meta:
        fields = "__all__"
        model = Selection


class SelectionListSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        fields = ["author", "name"]
        model = Selection


class SelectionCreateSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    def create(self, validated_data):
        request = self.context.get("request")
        print(request.user)
        validated_data["author"] = request.user
        return super().create(validated_data)

    class Meta:
        fields = "__all__"
        model = Selection
