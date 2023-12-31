from rest_framework import serializers
from watchlist.models import Movie


# Another way of field level validation
def name_lenght(value):
    if len(value) < 2:
        raise serializers.ValidationError("Name is too short!")


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_lenght])
    description = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
    
    # Object level validation
    def validate(self, data):
        if data["name"] == data["description"]:
            raise serializers.ValidationError("Name and Description should be different!")
        return data
    
    # Field level validation
    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short!")
    #     return value

