
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api import views

router = DefaultRouter()
router.register('stream', views.StreamPlarformVS, basename='streamplatform')


urlpatterns = [
    path('list/', views.WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', views.WatchDetailAV.as_view(), name='movie-detail'),

    path('', include(router.urls)),

    path('<int:pk>/review-create/', views.ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', views.ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),

    path('reviews/', views.UserReview.as_view(), name='user-review-detail')
]
