import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad
from ads.serializers import *
from users.models import UserRoles


def main_view(request):
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Category
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        new_cat = Category.objects.create(name=data.get("name"))
        return JsonResponse({"id": new_cat.id, "name": new_cat.name})


class CatListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse([{"id": cat.id, "name": cat.name} for cat in self.object_list.order_by("name")], safe=False)


class CatDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse({"id": cat.id, "name": cat.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data.get("name")
        self.object.save()
        return JsonResponse({"id": self.object.id, "name": self.object.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        cat = self.get_object()
        super().delete(request, *args, **kwargs)
        return JsonResponse({"id": cat.id})


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        if request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            return True


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by("-price")
    default_serializer_class = AdSerializer

    default_permission = [AllowAny]
    permissions = {
        "retrieve": [IsAuthenticated],
        "update": [IsAuthenticated, IsAuthor | IsStaff],
        "partial_update": [IsAuthenticated, IsAuthor | IsStaff],
        "destroy": [IsAuthenticated, IsAuthor | IsStaff]
    }

    serializers = {
        "list": AdListSerializer,
        "create": AdListSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist("cat")
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)

        text = request.GET.get("text")
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get("location")
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get("price_from")
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get("price_to")
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.order_by("name")
    default_serializer_class = SelectionSerializer

    default_permission = [AllowAny]
    permissions = {
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsAuthor],
        "partial_update": [IsAuthenticated, IsAuthor],
        "destroy": [IsAuthenticated, IsAuthor]
    }

    serializers = {
        "list": SelectionListSerializer,
        "create": SelectionCreateSerializer,
        "retrieve": SelectionDetailSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]
