from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from ads.models import Ad, Category
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
