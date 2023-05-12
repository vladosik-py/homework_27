from django.urls import path
from rest_framework import routers

from ads.views import *

urlpatterns = [
    path('', main_view),
    path('cat/', CatListView.as_view(), name="all_category"),
    path('cat/<int:pk>/', CatDetailView.as_view(), name="category_detail"),
    path('cat/create/', CatCreateView.as_view(), name="category_create"),
    path('cat/<int:pk>/update/', CatUpdateView.as_view()),
    path('cat/<int:pk>/delete/', CatDeleteView.as_view())
]

router = routers.SimpleRouter()
router.register('ads', AdViewSet)
urlpatterns = router.urls

router_1 = routers.SimpleRouter()
router.register('selection', SelectionViewSet)
urlpatterns = router.urls