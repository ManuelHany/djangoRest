from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
     
     class Meta:
           model = Review
           exclude = ['watchlist',]
        #   fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

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
            field_kwargs = {"view_name": 'stream-detail'}
            return field_class, field_kwargs
        



          
# def name_length(value): # 2
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharFie ld(validators=[name_length]) # 1
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, valicated_data):
#         return Movie.objects.create(**valicated_data)
    
#     def update(self, instance, validated_data):
#         """
#         put or patch
#         Args:
#             instance (Movie): old update
#             validated_data (Movie): new update
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
    
#     def validate(self, data): # 4 (object level validator)
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and Description should be different!")
#         else:
#             return data
    
#     # 3 (field type valicator)
#     # def validate_name(self, value):
        
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name is too short!")
#     #     else:
#     #         return value