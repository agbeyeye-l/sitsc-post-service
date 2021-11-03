from django.urls import path, include
from gallery import views

 

urlpatterns = [
    path('', views.GalleryCreateList.as_view(), name='gallery-list'),
    path('<int:pk>/', views.GalleryDetail.as_view(), name='gallery-detail'),
    path('user/<int:user_id>/', views.GalleryByUserAPIView.as_view(), name='gallery-by-user'),
]