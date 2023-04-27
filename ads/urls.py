from django.urls import path

from ads.views import *

urlpatterns = [
    path('', main_view),
    path('cat/', CatListView.as_view(), name="all_category"),
    path('cat/<int:pk>/', CatDetailView.as_view(), name="category_detail"),
    path('cat/create/', CatCreateView.as_view(), name="category_create"),
    path('cat/<int:pk>/update/', CatUpdateView.as_view()),
    path('cat/<int:pk>/delete/', CatDeleteView.as_view()),
    path('ad/', AdListView.as_view(), name="all_category"),
    path('ad/<int:pk>/', AdDetailView.as_view(), name="category_detail"),
    path('ad/create/', AdCreateView.as_view(), name="category_create"),
    path('ad/<int:pk>/update/', AdUpdateView.as_view()),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view()),

    path('ad/<int:pk>/upload_image/', AdUploadImage.as_view())
]
