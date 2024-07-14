from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
     review_user = serializers.StringRelatedField(read_only=True)
     class Meta:
           model = Review
           exclude = ['watchlist',]
        #   fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = "__all__"


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
        watchlist = WatchListSerializer(many=True, read_only=True)
        # watchlist = serializers.StringRelatedField(many=True)
        # watchlist = serializers.HyperlinkedRelatedField(
        #      many=True,
        #      read_only=True,
        #      view_name='movie-detail' 
        # )
            

        class Meta:
            model = StreamPlatform
            fields = "__all__"



        def build_url_field(self, field_name, model_class):
            field_class = self.serializer_url_field
            field_kwargs = {"view_name": 'streamplatform-detail'}
            return field_class, field_kwargs
        