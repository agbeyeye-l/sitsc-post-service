from django.urls import path, include
from post import views


urlpatterns = [
    path('', views.PostAPIView.as_view(), name='post-list'),
    path('<int:pk>/', views.PostDetailAPIView.as_view(), name='post-detail'),
    path('comment/', views.CommentCreateAPIView.as_view(), name='comment-create'),
    path('<int:post_id>/comment/', views.CommentListAPIView.as_view(), name='comment-list'),
    path('comment/<int:pk>/', views.CommentDetailAPIView.as_view(), name='comment-detail'),
    path('user-post/<int:id>/', views.PostByUserAPIView.as_view(), name='post-by-user'),
    path('search/<str:search_text>/', views.SearchPostAPIView.as_view(), name='search-post')
]
