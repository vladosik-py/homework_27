from django.urls import path

from ads.views import *

urlpatterns = [
    path('', main_view),
    path('cat/', CatView.as_view()),
    path('cat/<int:pk>/', CatDetailView.as_view()),
    path('ad/', AdView.as_view()),
    path('ad/<int:pk>/', AdDetailView.as_view()),
]
