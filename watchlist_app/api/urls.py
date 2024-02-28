
from django.urls import path, include
# from watchlist_app.api.views import movie_list, movie_details
<<<<<<< Updated upstream
from watchlist_app.api.views import ReviewList, ReviewDetail, WatchListAV, WatchDetailAV, StreamPlatformAV, StreamPlatformDetailAV
=======
from watchlist_app.api.views import (ReviewList, ReviewDetail, WatchListAV, 
                                     WatchDetailAV, StreamPlatformAV, 
                                     StreamPlatformDetailAV)
>>>>>>> Stashed changes

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>', WatchDetailAV.as_view(), name='movie-detail'),
    path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='stream-detail'),

<<<<<<< Updated upstream
    path('review', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail')
=======
    path('review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),

    # path('stream/<int:pk>/review', StreamPlatformDetailAV.as_view(), name='stream-detail'),
    # path('stream/review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
>>>>>>> Stashed changes
]
