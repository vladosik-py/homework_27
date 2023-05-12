from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from users.models import User, Location


class LocationSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Location


class UserSerializer(ModelSerializer):
    class Meta:
        exclude = ["password"]
        model = User


class UserListSerializer(ModelSerializer):
    # total_ads = SerializerMethodField()
    #
    # def get_total_ads(self, user):
    #     return user.ad_set.filter(is_published=True).count()
    total_ads = IntegerField()

    class Meta:
        exclude = ["password"]
        model = User


class UserCreateSerializer(ModelSerializer):
    location = SlugRelatedField(required=False, many=True, slug_field="name", queryset=Location.objects.all())

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop("location", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        passwd = validated_data.pop("password")
        new_user = User.objects.create(**validated_data)
        new_user.set_password(passwd)
        new_user.save()
        for loc_name in self._locations:
            loc, _ = Location.objects.get_or_create(name=loc_name)
            new_user.location.add(loc)
        return new_user

    class Meta:
        fields = "__all__"
        model = User


class UserUpdateSerializer(ModelSerializer):
    location = SlugRelatedField(required=False, many=True, slug_field="name", queryset=Location.objects.all())

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop("location", [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.location.clear()
        for loc_name in self._locations:
            loc, _ = Location.objects.get_or_create(name=loc_name)
            user.location.add(loc)
        return user

    class Meta:
        fields = "__all__"
        model = User
