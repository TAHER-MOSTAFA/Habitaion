import json
from habitation.ads.models import AD, Favourites, Image
from rest_framework import serializers
from django.contrib.gis.geos import Point
from json import loads as json_loads


class LocationPointSerializer(serializers.ListField):
    def to_representation(self, value):
        return value.coords

    def to_internal_value(self, *args, **kwargs):
        data = super().to_internal_value(*args, **kwargs)
        return Point(data)

class DistanceSerializer(serializers.Field):
    def to_representation(self, value):
        print(value, type(value))
        return "{:.2f}".format(value)


class ADSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    location = LocationPointSerializer(child=serializers.DecimalField(max_digits=20, decimal_places=5))
    lord = serializers.HiddenField(default=serializers.CurrentUserDefault())
    distance = DistanceSerializer(source='distance.km', required=False, read_only=True)
    is_fav = serializers.BooleanField(read_only=True, default=True)
    
    class Meta:
        model = AD
        fields = '__all__'

    def create(self, validated_data):
        images = validated_data.pop("images", [])        
        obj = super().create(validated_data)

        Image.objects.bulk_create([
            Image(image=img, ad_id=obj.id)
            for img in images
        ])
        return obj

    def to_representation(self, instance):
        data = super().to_representation(instance)
        images = instance.images.all()
        data.update(
            images = [img.image.url for img in images]
        )
        return data

class FavouriteSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ad_id = serializers.PrimaryKeyRelatedField(queryset=AD.objects, write_only=True)
    ad = ADSerializer(read_only=True, required=False)
    class Meta:
        model = Favourites
        fields = ['id', 'user', 'ad_id', 'ad', ]
    
    def create(self, validated_data):
        return Favourites.objects.create(user=validated_data['user'], ad=validated_data['ad_id'])
