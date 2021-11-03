from django.urls import path, include
from stories import views



urlpatterns = [
    path('', views.StoryList.as_view(), name='story-list'),
    path('<int:pk>/', views.StoryDetail.as_view(), name='story-detail'),
]