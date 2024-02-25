from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform


 
class WatchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchList
        fields = "__all__"



class StreamPlatformSerializer(serializers.ModelSerializer):
        watchlist = WatchListSerializer(many=True, read_only=True)
        
        class Meta:
            model = StreamPlatform
            fields = "__all__"

          
# def name_length(value): # 2
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length]) # 1
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