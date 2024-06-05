from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.validators import ValidationError
from rest_framework.views import APIView

from watchlist_app.api import serializers
from watchlist_app.api.pagination import WatchListCPagination
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.api.throttling import ReviewCreateThrottle
from watchlist_app.models import WatchList, StreamPlatform, Review


class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'review-detail'

    # def get_queryset(self):
    #     """
    #         This is the Second Filter Method
    #         We are mapping the value of username instead of the number of it
    #     """
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username) # because review user is a foreign key I have to ecplain what does this FK mean for you.

    def get_queryset(self):
        """
            This is the Third Filter Method
            instead of directly mapping the value we are mapping the parameter
        """
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username) # because review user is a foreign key I have to ecplain what does this FK mean for you.

class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]


    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        # print(review_queryset.exists())
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")


        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'review-detail'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'



class StreamPlarformVS(viewsets.ViewSet):
    """
    A simple view set for listing or retrieving users.
    """
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializer(queryset, many=True, context= {"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        watchlist = get_object_or_404(queryset, pk=pk)
        serializer = serializers.StreamPlatformSerializer(watchlist, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        # return Response({}, 200)
        stream_platform = StreamPlatform.objects.get(pk=pk)
        serializer = serializers.StreamPlatformSerializer(stream_platform, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        stream_platform = StreamPlatform.objects.get(pk=pk)
        stream_platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
    def create(self, request):
        serializer = serializers.StreamPlatformSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    # def delete(self, request, pk=None):
    #     stream_platform = StreamPlatform.objects.get(pk=pk)
    #     serializer = StreamPlatformSerializer(stream_platform, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.delete()


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = serializers.WatchListSerializer(movies, many=True)
        return Response(serializer.data)
    

    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put (self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = serializers.WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
